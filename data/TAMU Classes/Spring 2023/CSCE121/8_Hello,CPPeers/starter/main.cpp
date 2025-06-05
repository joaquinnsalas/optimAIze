# include <iostream>
# include <string>
# include <stdexcept>
# include "Network.h"

using std::cout, std::cin, std::endl, std::string, std::vector;

void printMenu() {  // this is the frontend interaction with the backend.
    cout << "Welcome to Gather" << endl;
    cout << "The options are: " << endl;
    cout << "1. load data file and add information" << endl;
    cout << "2. show posts by user" << endl;
    cout << "3. show posts with hashtag" << endl;
    cout << "4. show most popular hashtag" << endl;
    cout << "9. quit" << endl;
    cout << "--------> Enter your option: ";
}

void processLoad(Network& cppeers) {
    string fileName = "";
    cout << "Enter filename: ";
    cin >> fileName;
    cppeers.loadFromFile(fileName);
}

void processPostsByUser(Network& cppeers) {
    // TODO: implement
    string userName = ""; //Get the user theyre searching for
    cout << "Enter username: ";
    cin >> userName;

    std::vector<Post*> userpost = cppeers.getPostsByUser(userName);
    for (size_t i = 0; i < userpost.size(); i++) {
        cout << userpost.at(i)->getPostText() << endl;
    }
}

void processPostsWithHashtags(Network& cppeers) {
    // TODO: implement
    string hashtag = "";
    cout << "Enter tagname: ";
    cin >> hashtag;

    std::vector<Post*> hashtags = cppeers.getPostsWithTag(hashtag);
    for (size_t i = 0; i < hashtags.size(); i++) {
        cout << hashtags.at(i)->getPostText() << endl;
    } 
}

void processMostPopularHashtag(Network& cppeers) {
    // TODO: implement
    std::vector<string> populartag = cppeers.getMostPopularHashtag();
    for (size_t i = 0; i < populartag.size(); i++) {
        cout << populartag.at(i) << endl;
    }
}

int main() {
    // Switch here to bring the frontend interatction to the backend.

    try {
        Network cppeers;

        int choice = 0;

        do {
            printMenu();
            cin >> choice;
            switch(choice) {
                case 1: {
                    processLoad(cppeers);
                    break;
                }
                case 2: {
                    processPostsByUser(cppeers);
                    break;
                }
                case 3: {
                    processPostsWithHashtags(cppeers);
                    break;
                }
                case 4: {
                    processMostPopularHashtag(cppeers);
                    break;
                }
            }
        } while (choice != 9);
    } catch (std::exception& exc) {
        std::cout << exc.what() << endl;
    }
    
    return 0;
}
