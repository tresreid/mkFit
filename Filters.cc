#include "Filters.h"

#include "Simulation.h"
#include "KalmanUtils.h"
#include "seedtest.h"
#include "buildtest.h"
#include "fittest.h"
#include "ConformalUtils.h"
#include "TrackerInfo.h"

#include "Track.h"
#include "Validation.h"
#include "Geometry.h"
#include "BinInfoUtils.h"
#include "Config.h"

//#define DEBUG
#include "Debug.h"

#ifdef TBB
#include "tbb/tbb.h"
#endif


#include <memory>


// using namespace mkfit;
using namespace tbb;
using namespace std;


//make_filter<inputType,outputType>(mode,functor).
//ntoken = number of things that can be in flight
void RunPipeline(int ntoken, const TrackVec & seedTracks_, int _ts, std::vector<bool> & writetrack) {
    tbb::parallel_pipeline(
        ntoken,
        tbb::make_filter<void,TrackForFilter*>(
            tbb::filter::serial_in_order, MyInputFunc(seedTracks_, _ts) )
    &
        tbb::make_filter<TrackForFilter*,TrackForFilter*>(
            tbb::filter::parallel, ContFilter_1() )
    &
        tbb::make_filter<TrackForFilter*,void>(
            tbb::filter::serial_in_order, MyOutputFunc(writetrack) ) 
    );
} 

/*************************************************************************************************************/

//    Input functions

/*************************************************************************************************************/


MyInputFunc::MyInputFunc(const TrackVec & seedTracks_, int _ts, int _ns) {
    sT = seedTracks_;
    ts = _ts;
    ns = _ns;
}
 
MyInputFunc::MyInputFunc( const MyInputFunc& f ) {
    sT = f.sT;
    ts = f.ts;
    ns = f.ns;
}
 
MyInputFunc::~MyInputFunc() {
}
 
TrackForFilter MyInputFunc::operator()( tbb::flow_control& fc ) {

    // base case
    if(TSS >= ns){
        fc.stop();
    } else {
        struct TrackForFilter track;

        track.tk    = sT[ts];
        track.ts    = ts;
        track.tkk   = sT[TSS];
        track.tss   = TSS;
        track.cont  = false;
        track.wire  = true;
        track.ns    = ns;

        TSS++;
        return track;
    }

}



/*************************************************************************************************************/

//    Continue functions

/*************************************************************************************************************/




struct TrackForFilter MyTransformFunc::operator()( struct TrackForFilter inTrack ) {
    // Add terminating null so that strtol works right even if number is at end of the input.
    struct TrackForFilter newTrack;

    outTrack.tk    = inTrack.tk;
    outTrack.ts    = inTrack.ts;
    outTrack.tkk   = inTrack.tkk;
    outTrack.tss   = inTrack.tss;
    outTrack.cont  = inTrack.tkk.nFoundHits() < minNHits;
    outTrack.wire  = inTrack.wire;
    outTrack.ns    = inTrack.ns;

    return out;
} 





/*************************************************************************************************************/

//    Output functions

/*************************************************************************************************************/


MyOutputFunc::MyOutputFunc( std::vector<bool> & _writetrack ) {
  writetrack = _writetrack;
}


MyOutputFunc::MyOutputFunc( MyOutputFunc& f ) {
  writetrack = f.writetrack;
}


void MyOutputFunc::operator()( struct TrackForFilter inTrack ) {
    
    writetrack[inTrack.tss] = inTrack.wire;    

} 
