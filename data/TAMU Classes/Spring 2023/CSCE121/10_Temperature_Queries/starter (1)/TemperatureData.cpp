# include "TemperatureData.h"
using std::string;

TemperatureData::TemperatureData() : id{""}, year{0}, month{0}, temperature{0.0} /* TODO */ {
	// TODO: implement this function
}

TemperatureData::TemperatureData(string id, int year, int month, double temperature) : id{id}, year{year}, month{month}, temperature{temperature} /* TODO */ {
	// TODO: implement this function
}

TemperatureData::~TemperatureData() {}

bool TemperatureData::operator<(const TemperatureData& b) {
	// TODO: implement this function
	if (this->id < b.id) {
		return true;
	}
	else if (this->id > b.id) {
		return false;
	}
	if (this->year < b.year) {
		return true;
	}
	else if (this->year > b.year) {
		return false;
	}
	if (this->month < b.month) {
		return true;
	}
	else if (this->month > b.month) {
		return false;
	}
	if (this->temperature < b.temperature) {
		return true;
	}
	// if (this->temperature > b.temperature) {
	// 	return false;
	// }
	return false;
}

