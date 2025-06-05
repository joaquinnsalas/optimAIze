# include <iostream>
# include <fstream>
# include <sstream>
# include <stdexcept>
# include <vector>
# include <string> //to use getline
# include <cctype> //to user .tolower()
# include "Network.h"

using std::string;
using std::vector;
using std::exception;

Network::Network() : users({}), posts({}), tags({}) {}

void Network::loadFromFile(string fileName) { //If theres a problwm later its this function
    // TODO: load user and post information from file
    std::ifstream myfile(fileName);

    if (!myfile.is_open()) {
        throw std::invalid_argument("Unable to open file.");
    }
    string type= "";
    string userName= "";
    string postText = "";
    unsigned int postId = 0;
    string e = "";
    string post = "";

    //read all the inputs until EOF
    while (!myfile.eof()) {

        //get the first word in the line
        myfile >> type;

        if (type == "User") {
            myfile >> userName;
            try {
                addUser(userName);
            }
            catch (exception& ex) {
                throw std::runtime_error("Invalid User.");
            }
        } else if (type == "Post") {
            myfile >> postId >> userName;

            std::getline(myfile, postText); // problem here i need to append its not getting the post right
            std::getline(myfile, e); //i think theres a empty line in the test files (this fixed it)
            std::stringstream ss(postText);

            ss >> post; //get the first word

            while (ss >> postText) {
                post += " " + postText; //append all after
            }
             // std::cout << postId << " " << userName << " " << postText << std::endl;
            try {
                addPost(postId, userName, postText);
            }
            catch (exception& ex) {
                throw std::runtime_error("Invalid Post.");
            }

        } else if (myfile.fail()) { //For bad file format
            throw std::invalid_argument("Incorrect file format.");
        }
    }
}

void Network::addUser(string userName) {
    // TODO: create user and add it to network

    //make the usernames lowercase to compare
    size_t length = userName.size();
    for (size_t i = 0; i < length; i++) {
        userName.at(i) = tolower(userName.at(i));
    }
    // std::cout << "Username lowercase " << userName << std::endl;
    size_t usersize = users.size();
    for (size_t i = 0; i < usersize; i++) {
        if (userName == users.at(i)->getUserName()) { //point to the username im checking
            throw std::invalid_argument("User already exists.");
        }
    }
    User* newuser = new User(userName); //new user object
    users.push_back(newuser); //add to vector
    std::cout << "Added User " << userName << std::endl; //To console the goods
}

void Network::addPost(unsigned int postId, string userName, string postText) {
    // TODO: create post and add it to network

    for (size_t i = 0; i < posts.size(); i++) {
        if (postId == posts.at(i)->getPostId()) {
            throw std::invalid_argument("Post with this id already exists.");
        }
    }
    //check if the user exists in the system
    bool userexists = false;
    size_t j = 0; //initialize outside because j associates user to post
    for (j = 0; j < users.size(); j++) {
        if (userName == users.at(j)->getUserName()) {
            userexists = true;
            break;
        }
    }
    if (!userexists) {
        throw std::invalid_argument("This user does not exist.");
    }
    //create a new post
    Post* newpost = new Post(postId, userName, postText);
    posts.push_back(newpost); //add post to Network data post

    for (size_t u = 0; u < users.size(); u++) {
        if (userName == users.at(u)->getUserName()) {
            users.at(j)->addUserPost(newpost);
        }
    }

    //Extract candidate hashtags contained in the post
    vector<string> hashtag = newpost->findTags();

    // for (size_t k = 0; k < hashtag.size(); k++) { //searching through
    //     bool istagthere = false;
    //     for (size_t l = 0; l < tags.size(); l++) {
    //         std::cout << "Invalid hashtag " << hashtag.at(k) << std::endl;
    //         if (tags.at(l)->getTagName() == hashtag.at(k));
    //             istagthere = true;
    //             tags.at(l)->addTagPost(newpost);
    //     }
    //     if (!istagthere) { //creating
    //         try{
    //             Tag *newtag = new Tag(hashtag.at(k));
    //             newtag->addTagPost(newpost);
    //             tags.push_back(newtag);
    //         } catch (std::exception &e) {
    //             continue;
    //         }
    //     }
    // }
}

vector<Post*> Network::getPostsByUser(string userName) {
    // TODO: return posts created by the given user
    if (userName.empty()) {
        throw std::invalid_argument("bad stuff");
    }
    vector<Post*> userpost;

    for (size_t i = 0; i < posts.size(); i++) { //iterate through all the users
        if (userName == posts.at(i)->getPostUser()) { //find the user that was passed in
            userpost.push_back(posts.at(i));
        }
    }
    return userpost;
}

vector<Post*> Network::getPostsWithTag(string tagName) {
    // TODO: return posts containing the given tag

    std::cout << tagName << std::endl;

    if (tagName.empty()) {
        throw std::invalid_argument("tagName empty.");
    }
    bool tagexist = false;
    size_t index = 0; //same check from above
    for (size_t i = 0; i < tags.size(); i++) {
        if (tagName == tags.at(i)->getTagName()) {
            tagexist = true;
            index = i;
            break;
        }
    }
    std::cout << tagexist << std::endl;
    if (!tagexist) {
        throw std::invalid_argument("tagName not found.");
    }

    return tags.at(index)->getTagPosts();
    //find all the posts with that tag
    // vector<Post*> tagPost = tags.at(i)->getTagPosts();
    // vector<Post*> postsWithTag;

    // size_t tplen = tagPost.size();
    // for (size_t j = 0; j < tplen; j++) {
    //     Post* thesepost = tagPost.at(i);
    //     for (size_t k = 0; k < posts.size(); k++) {
    //         if (posts->get)
    //     }
    // }

    // return postsWithTag; getPos
}

vector<string> Network::getMostPopularHashtag() {
    // TODO: return the tag occurring in most posts

    vector<string> mostpopular;
    size_t times = 0;

    for (size_t i = 0; i < tags.size(); i++) {
        string tag = tags.at(i)->getTagName();
        size_t tagcount = 0;
    }
    return mostpopular;
}

Network::~Network() {
    for (unsigned int i = 0; i < users.size(); ++i) {
        delete users.at(i);
    }

    for (unsigned int i = 0; i < tags.size(); ++i) {
        delete tags.at(i);
    }
    
    for (unsigned int i = 0; i < posts.size(); ++i) {
        delete posts.at(i);
    }
}
