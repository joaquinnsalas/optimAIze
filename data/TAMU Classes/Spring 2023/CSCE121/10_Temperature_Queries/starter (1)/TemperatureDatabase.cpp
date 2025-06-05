# include "TemperatureDatabase.h"
# include <fstream>
# include <iostream>
# include <sstream> //for bringing in data

using std::cout, std::endl, std::string, std::ofstream, std::ifstream;

TemperatureDatabase::TemperatureDatabase() {}
TemperatureDatabase::~TemperatureDatabase() {}

void TemperatureDatabase::loadData(const string& filename) {
	// TODO: implement this function

	ifstream myfile(filename);

	if (!myfile.is_open()) {
		cout << "Error: Unable to open " << filename << endl;
		return;
	}
	//bring in the lines
	while (true) {

		string id = "";
		int year = 0;
		int month = 0;
		double temperature = 0.0;
		string thisstring = "";
		getline(myfile, thisstring);

		if (myfile.eof()) {
			break;
		}

		std::stringstream ss;
		ss << thisstring;
		ss >> id >> year >> month >> temperature;
		if (ss.fail()) {
			cout << "Error: Other invalid input " << endl;
			continue;
		}
		if ((month < 1) || (month > 12)) {
			cout << "Error: Invalid month "  << month << endl;
			continue;
		}
		if ((year < 1800) || (year > 2023)) {
			cout << "Error: Invalid year "  << year << endl;
			continue;
		}
		if (temperature == -99.99) {
			continue;
		}
		if ((temperature < -50.0) || (temperature > 50.0)) {
			cout << "Error: Invalid temperature "  << temperature << endl;
			continue;
		}
		records.insert(id, month, year, temperature);
	}
	myfile.close();
}

void TemperatureDatabase::outputData(const string& filename) {
	ofstream dataout("sorted." + filename);
	
	if (!dataout.is_open()) {
		cout << "Error: Unable to open " << filename << endl;
		exit(1);
	}

	dataout << records.print();
}

void TemperatureDatabase::performQuery(const string& filename) {
	// TODO: implement this function
}
