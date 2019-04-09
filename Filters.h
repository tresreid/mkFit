

#include "tbb/task_arena.h"
#include "tbb/parallel_for.h"
#include "tbb/enumerable_thread_specific.h"

// for pipeline
#include "tbb/compat/thread"
#include "tbb/pipeline.h"

using namespace tbb;
using namespace std;

//make_filter<inputType,outputType>(mode,functor).
//ntoken = number of things that can be in flight
void RunPipeline( int ntoken, FILE* input_file, FILE* output_file ) {
    tbb::parallel_pipeline(
        ntoken,
        tbb::make_filter<void,TextSlice*>(
            tbb::filter::serial_in_order, MyInputFunc(input_file) )
    &
        tbb::make_filter<TextSlice*,TextSlice*>(
            tbb::filter::parallel, MyTransformFunc() )
    &
        tbb::make_filter<TextSlice*,void>(
            tbb::filter::serial_in_order, MyOutputFunc(output_file) ) 
    );
} 

/*************************************************************************************************************/


// Functor that writes a TextSlice to a file.
class MyOutputFunc {
    FILE* my_output_file;
public:
    MyOutputFunc( FILE* output_file );
    void operator()( TextSlice* item ) const;
};
 
MyOutputFunc::MyOutputFunc( FILE* output_file ) :
    my_output_file(output_file)
{
}
 
void MyOutputFunc::operator()( TextSlice* out ) const {
    size_t n = fwrite( out->begin(), 1, out->size(), my_output_file );
    if( n!=out->size() ) {
        fprintf(stderr,"Can't write into file '%s'\n", OutputFileName);
        exit(1);
    }
    out->free();
} 


/*************************************************************************************************************/


// Functor that changes each decimal number to its square.
class MyTransformFunc {
public:
    TextSlice* operator()( TextSlice* input ) const;
};

TextSlice* MyTransformFunc::operator()( TextSlice* input ) const {
    // Add terminating null so that strtol works right even if number is at end of the input.
    *input->end() = '\0';
    char* p = input->begin();
    TextSlice* out = TextSlice::allocate( 2*MAX_CHAR_PER_INPUT_SLICE );
    char* q = out->begin();
    for(;;) {
        while( p<input->end() && !isdigit(*p) )
            *q++ = *p++;
        if( p==input->end() )
            break;
        long x = strtol( p, &p, 10 );
        // Note: no overflow checking is needed here, as we have twice the
        // input string length, but the square of a non-negative integer n
        // cannot have more than twice as many digits as n.
        long y = x*x;
        sprintf(q,"%ld",y);
        q = strchr(q,0);
    }
    out->set_end(q);
    input->free();
    return out;
} 


/*************************************************************************************************************/



TextSlice* next_slice = NULL;

class MyInputFunc {
public:
    MyInputFunc( FILE* input_file_ );
    MyInputFunc( const MyInputFunc& f ) : input_file(f.input_file) { }
    ~MyInputFunc();
    TextSlice* operator()( tbb::flow_control& fc ) const;
private:
    FILE* input_file;
};
 
MyInputFunc::MyInputFunc( FILE* input_file_ ) :
    input_file(input_file_) { }
 
MyInputFunc::~MyInputFunc() {
}
 
TextSlice* MyInputFunc::operator()( tbb::flow_control& fc ) const {
    // Read characters into space that is available in the next slice.
    if( !next_slice )
        next_slice = TextSlice::allocate( MAX_CHAR_PER_INPUT_SLICE );
    size_t m = next_slice->avail();
    size_t n = fread( next_slice->end(), 1, m, input_file );
    if( !n && next_slice->size()==0 ) {
        // No more characters to process
        fc.stop();
        return NULL;
    } else {
        // Have more characters to process.
        TextSlice* t = next_slice;
        next_slice = TextSlice::allocate( MAX_CHAR_PER_INPUT_SLICE );
        char* p = t->end()+n;
        if( n==m ) {
            // Might have read partial number.  
            // If so, transfer characters of partial number to next slice.
            while( p>t->begin() && isdigit(p[-1]) )
                --p;
            assert(p>t->begin(),"Number too large to fit in buffer.\n");
            next_slice->append( p, t->end()+n );
        }
        t->set_end(p);
        return t;
    }
}

