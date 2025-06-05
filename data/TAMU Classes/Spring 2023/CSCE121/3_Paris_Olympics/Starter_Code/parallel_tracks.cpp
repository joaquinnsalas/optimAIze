#include <iostream>
#include <iomanip>
#include <string>
#include "parallel_tracks.h"

using std::string;
using std::cout;
using std::endl;
using std::cin;
using std::cerr;

//-------------------------------------------------------
// Name: get_runner_data
// PreCondition:  the prepped parallel arrays
// PostCondition: all arrays contain data from standard in
//---------------------------------------------------------
bool get_runner_data( double timeArray[], std::string countryArray[], 
		unsigned int numberArray[], std::string lastnameArray[]) 
{
  //TODO
  // Update function to return the correct boolean values based on the parameters
	for (int i = 0; i < 9; i++) {

		cin >> timeArray[i];
		cin >> countryArray[i];
		cin >> numberArray[i];
		cin >> lastnameArray[i];

		if (timeArray[i] <= 0.0) {
			//cout << "1" << endl;
			return false;
		}
		int lengthCountry = countryArray[i].length();
		if (lengthCountry != 3) {
			//cout << "2" << endl;
			return false;
		}
		for (int j = 0; j < lengthCountry; j++) {

			if (!isalpha(countryArray[i][j]) || (!isupper(countryArray[i][j]))) {
				//cout << "3" << endl;
				return false;
			}
		}
		if (numberArray[i] >= 100) {
			//cout << "4" << endl;
			return false;
		}
		int lengthName = lastnameArray[i].length();
		if (lengthName <= 1) {
			//cout << "Invalid last name" << endl;
			return false;
		}
		for (int k = 0; k < lengthName; k++) {
			if (!isalpha(lastnameArray[i][k])) {
				//cout << "5" << endl;
				return false;	
			}
		}
		if (isupper(lastnameArray[i][0] == false)) {
			//cout << "6" << endl;
			return false;
		}
	}
	return true;// set so it will compile
}

//-------------------------------------------------------
// Name: prep_double_array
// PreCondition:  an array of doubles is passed in
// PostCondition: data in the array is 'zeroed' out
//---------------------------------------------------------
void prep_double_array(double ary[])
// making sure all values within the array are set to 0.0;
{
  //TODO
  for (int i = 0; i < 9; i++) {
  	ary[i] = 0.0;
  }
}
//-------------------------------------------------------
// Name: prep_unsigned_int_array
// PreCondition:  an array of unsigned ints is passed in
// PostCondition: data in the array is 'zeroed' out
//---------------------------------------------------------
void prep_unsigned_int_array(unsigned int ary[])
// making sure all values within the array are set to 0;
{
	//TODO
	for (int i = 0; i < 9; i++) {
		ary[i] = 0;
	}
}
//-------------------------------------------------------
// Name: prep_string_array
// PreCondition:  an array of strings is passed in
// PostCondition: each element in the array is set to "N/A"
//---------------------------------------------------------
void prep_string_array(std::string ary[])
// making sure all values within the array are set to "N/A";
{
	//TODO
	for (int i = 0; i < 9; i++) {
		ary[i] = "N/A";
	}
}
//-------------------------------------------------------
// Name: get_ranking
// PreCondition:  just the time array is passed in, and has valid data
// PostCondition: after a very inefficient nested loop to determine the placements 
// and places the ranks in a new array. That new array is returned
//---------------------------------------------------------
void get_ranking(const double timeArray[], unsigned int rankArray[])
{
	//TODO
	//create a algorithm to find the lowest time and set it to 1 and second lowest time set to 2, etc.
	const unsigned int SIZE = 9;
	double minTime;
	double maxTime = -1;
	unsigned int rank = 1;
	int slot;

	while(rank <= SIZE) {

		minTime = 99999999;
		for (unsigned int i = 0; i < SIZE; i++) {

			if (rankArray[i] == 0) { //if rankArray is empty

				if ((timeArray[i] < minTime) && (timeArray[i] > maxTime)) { //if timeArray time is less than minTime and greater than maxTime
					minTime = timeArray[i]; //Save the time as minTime
					slot = i; 
				}
			}
		}
		rankArray[slot] = rank;
		rank++;
		maxTime = minTime;
	}
}
//-------------------------------------------------------
// Name: print_results
// PreCondition:  all parallel arrays are passed in and have valid data
// PostCondition: after a very inefficient nested loop to determine the ranks
// it then displays them along with a delta in time from the start
//---------------------------------------------------------
void print_results(const double timeArray[], const std::string countryArray[],
		const std::string lastnameArray[], const unsigned int rankArray[])
{

	std::cout << "Final results!!";
	std::cout << std::setprecision(2) << std::showpoint << std::fixed << std::endl;
	double best_time = 0.0;
		
	// print the results, based on rank, but measure the time difference_type
	for(unsigned int j = 1; j <= SIZE; j++)
	{
		
		// go thru each array, find who places in "i" spot
		for(unsigned int i = 0; i < SIZE; i++)
		{
			if(rankArray[i] == 1) // has to be a better way, but need the starting time
			{
				best_time = timeArray[i];
			}
			
			
			if(rankArray[i] == j) // then display this person's data
			{
				// this needs precision display
				std::cout << "[" << j << "]  " << timeArray[i] << " " << std::setw(15) << std::left << lastnameArray[i] << "\t" << "(" << countryArray[i] << ")  +" << (timeArray[i] - best_time) << std::endl; 
			}
		}
	}	
}

std::string trim(std::string ret) {
	// remove whitespace from the beginning
	while (!ret.empty() && isspace(ret.at(0))) {
			ret.erase(0, 1);
		}

	// remove whitespace from the end
	//  Note: last index is (.size() - 1) due to 0 based indexing
	while (!ret.empty() && isspace(ret.at(ret.size()-1))) {
		ret.erase(ret.size()-1, 1);
	}
	
	return ret;
}