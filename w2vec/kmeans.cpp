#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <algorithm>
using namespace std;

const int MAX_STRING = 500;

void load_dataset(const char* input_f, vector< vector<float> >& data, vector<string>& vocab)
{
	fstream fi;
        fi.open(input_f, ios::in);
	string line, wrd;
	float val, norm = 0;
        cout << "Loading dataset..." << endl;
        bool firstline = true;
        while (getline(fi, line, '\n')) {
                if (firstline) { firstline = false; continue ;}
		stringstream strin;
		strin << line;
		strin >> wrd;
		vocab.push_back(wrd);
		vector<float> sample;
		norm = 0.0;
		while (strin >> val) {
			sample.push_back(val);
			norm += (val * val);
		}
		// divide by two norm
		//for (int i = 0; i < sample.size(); i++) sample[i] /= sqrt(norm);
		data.push_back(sample);
	}
	fi.close();
        cout << "# of samples - " << vocab.size() << " , # dimension - " << data[0].size() << endl;	
        cout << "Loaded Dataset." << endl;
}

void run_kmeans(const vector< vector<float> >& data, const vector<string>& vocab, const char* output_f, const int& niter, const int& nclasses)
{
    // local vars
    int   ii, c, d, v, closeid;
    float closev, x, norm;

    // parameters 
    int   I = niter;
    int   V = vocab.size();
    int   C = nclasses;
    int   D = data[0].size();

    // memory for k-means - 4CD + 4C + 2V bytes 
    float      cent[C][D];
    int        centcn[C];
    int  cl[V];
    	     
    for (v = 0; v < V; v++) cl[v] = v % C;

    // overall time complexity - O(IVCD) - I - # of iterations, V - # of samples, C  - # of classes, D = dimension
    // O(10^8) ~= 1 sec . O(10^10) ~= 2 min
    for (ii = 0; ii < I; ii++) {
      printf("Iteration %d : \n", ii);

      // init - O(CD) time
      for (c = 0;  c < C; c++) {
         centcn[c] = 1;
	 for (d = 0; d < D; d++) cent[c][d] = 0.0;
      }

      // find the cluster center - O(VD) time
      for (v = 0; v < V; v++) {
        for (d = 0; d < D; d++) cent[cl[v]][d] += data[v][d];
        centcn[cl[v]]++;
      }

      // divide by # of cluster assgnments, l2-norm - O(2CD) time
      for (c = 0; c < C; c++) {
        norm = 0;
        for (d = 0; d < D; d++) {
          cent[c][d] /= (1.0 * centcn[c]);
          norm += cent[c][d] * cent[c][d];
        }
        norm = sqrt(norm);
        for (d = 0; d < D; d++) cent[c][d] /= norm;
      }

      // assign the class-label w.r.t cosine similarity - O(VCD) time 
      // TODO : parallel 
     
     for (v = 0; v < V; v++) {
        closev = -10;
        closeid = 0;
        for (c = 0; c < C; c++) {
          x = 0;
          for (d = 0; d < D; d++) x += cent[c][d] * data[v][d]; // cosine-similariy (as both are unit-norms)
          if (x > closev) {
            closev = x;
            closeid = c;
          }
        }
        cl[v] = closeid;
      }
    }
    // Save the K-means classes 
    fstream fo;
    fo.open(output_f, ios::out);
    vector< pair<int, string> > ans(V);
    for (v = 0; v < V; v++) ans[v] = make_pair(cl[v], vocab[v]);
    sort(ans.begin(), ans.end());
    
    // output
    fo << ans[0].second.c_str() ; 
    int prev_l = ans[0].first;
    for (v = 1; v < V; v++) {
	    int l = ans[v].first;
	    if (l == prev_l) {
		    fo << " " << ans[v].second.c_str();
	    } else {
		    fo << endl << ans[v].second.c_str();
	    }
	    prev_l = l;
    }
    fo.close(); 
}

int ArgPos(const char *str, int argc, char **argv) {
  int a;
  for (a = 1; a < argc; a++) if (!strcmp(str, argv[a])) {
    if (a == argc - 1) {
      printf("Argument missing for %s\n", str);
      exit(1);
    }
    return a;
 }
  return -1;
}

int main(int argc, char** argv) {

        
	if (argc == 1) {
	    printf("KMEANS CLUSTERING v 0.1\n");
	    printf("\nUsage : ./kmeans -input <input-file> -output <output-file> -nclasses 25 -niter 40\n\n");
	    return 0;
	} 
	int i;
	vector< vector<float> > data;
	vector< string > vocab;
        
	char input[MAX_STRING];
	char output[MAX_STRING]; 
	int nclasses  = 200;
	int niter     = 50;
        
	if ((i = ArgPos((char *)"-ncluster", argc, argv)) > 0) nclasses = atoi(argv[i + 1]);
        if ((i = ArgPos((char *)"-niter", argc, argv)) > 0)    niter    = atoi(argv[i + 1]);
        if ((i = ArgPos((char *)"-input", argc, argv)) > 0)    strcpy(input, argv[i+1]);
        if ((i = ArgPos((char *)"-output", argc, argv)) > 0)   strcpy(output, argv[i+1]);
        cout << "Parameters : " << endl;
        cout << "input:" << input << endl;
        cout << "output:" << output << endl;
        cout << "nclasses:" << nclasses << endl;
        cout << "niter:" << niter << endl;
        cout << "----------------------------------------------------------------------" << endl;
        
	load_dataset(input, data, vocab);
	run_kmeans(data, vocab, output, niter, nclasses);
}
