# include "Database.h"

using std::string, std::vector;

// TODO: implement constructor using member initializer list
Database::Database() : stateParkList({}), camperList({}) {}

Database::~Database() {
	for (unsigned int i = 0; i < stateParkList.size(); ++i) {
		delete stateParkList.at(i);
	}
	
	for (unsigned int i = 0; i < camperList.size(); ++i) {
		delete camperList.at(i);
	}
}

void Database::addStatePark(string parkName, double entranceFee, double trailMiles) {
	INFO(parkName)
	INFO(entranceFee)
	INFO(trailMiles)

	// TODO: implement function
	StatePark* park = new StatePark(parkName, entranceFee, trailMiles);
	stateParkList.push_back(park);
}

void Database::addPassport(string camperName, bool isJuniorPassport) {
	INFO(camperName)
	INFO(isJuniorPassport)

	// TODO: implement function
	Passport* passport = new Passport(camperName, isJuniorPassport);
	camperList.push_back(passport);
}

void Database::addParkToPassport(string camperName, string parkName) {
	INFO(camperName)
	INFO(parkName)

	StatePark* park = nullptr;
	Passport* camper = nullptr;

	for (StatePark *state : this->stateParkList) {
		if (state->getParkName() == parkName) {
			park = state;
			break;
		}
	}
	for (Passport *pass : this->camperList) {
		if (pass->getCamperName() == camperName) {
			camper = pass;
			break;
		}
	}
	camper->addParkVisited(park);
}

vector<string> Database::getParksInRevenueRange(double lowerBound, double upperBound) {
	INFO(lowerBound)
	INFO(upperBound)

	// TODO: (optional) implement function
	
	return {};
}

vector<string> Database::getHikersAtLeastLevel(int level) {
	INFO(level)

	// TODO: (optional) implement function

	return {};
}
