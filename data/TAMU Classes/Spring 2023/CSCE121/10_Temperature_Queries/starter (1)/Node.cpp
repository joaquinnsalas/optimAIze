# include <string>
# include "Node.h"

using std::string;

Node::Node() : next{nullptr}, data{TemperatureData()} { /* TODO */ // Default constructor
	// TODO: implement this function
}

Node::Node(string id, int year, int month, double temperature) : next{nullptr} {  /* TODO */ 
	// TODO: implement this function
	data.id = id;
	data.year = year;
	data.month = month;
	data.temperature = temperature;
}

bool Node::operator<(const Node& b) /* TODO */ {
	// TODO: implement this function
	if (this->data.id != b.data.id) {
		if (this->data.id < b.data.id) {
			return true;
		}
	}
	else if (this->data.year != b.data.year) {
		if (this->data.year < b.data.year) {
			return true;
		}
	}
	else if (this->data.month != b.data.month) {
		if (this->data.month < b.data.month) {
			return true;
		}
	}
	else if (this->data.temperature != b.data.temperature) {
		if (this->data.temperature < b.data.temperature) {
			return true;
		}
	}
	else {
		return false;
	}
	return false;
}
