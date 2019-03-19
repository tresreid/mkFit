#ifndef __FILTERS_H__
#define __FILTERS_H__

#include "Event.h"

#include "Track.h"
#include "Validation.h"
#include "Geometry.h"
#include "BinInfoUtils.h"
#include "Config.h"

#include "tbb/task_arena.h"
#include "tbb/parallel_for.h"
#include "tbb/enumerable_thread_specific.h"

// for pipeline
#include "tbb/compat/thread"
#include "tbb/pipeline.h"

// using namespace mkFit;
using namespace tbb;
using namespace std;

struct TrackForFilter {
    Track tk;
    int   ts;
    Track tkk;
    int   tss;
    bool  cont;
    bool  wire;
};



/*************************************************************************************************************/

// Funciton that starts the pipeline
int TSS = 0; // this is a weird globalish thing that we need? to keep track

class MyInputFunc {
public:
    MyInputFunc(const TrackVec & seedTracks_, int _ts);
    MyInputFunc( const MyInputFunc& f );
    ~MyInputFunc();
    struct TrackForFilter operator()( tbb::flow_control& fc );
private:
    const TrackVec sT;
    int ts;
};
 

/*************************************************************************************************************/


// Functor that is in the middle of the pipe
class ContFilter_1 {
public:
    TrackForFilter* operator()( struct TrackForFilter* inTrack );
};


/*************************************************************************************************************/


// Functor that ends the pipeline.
class MyOutputFunc {
public:
    MyOutputFunc( std::vector<bool> & _writetrack );
    MyOutputFunc( MyOutputFunc& f );
    void operator()( struct TrackForFilter* inTrack );
private:
    std::vector<bool> writetrack;
};
 

#endif
