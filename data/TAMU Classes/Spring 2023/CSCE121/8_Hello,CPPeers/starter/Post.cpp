# include <iostream>
# include <string>
# include <stdexcept>
# include <cctype> //to user .tolower()
# include <sstream>
# include "Post.h"

using std::string;
using std::vector;
using std::stringstream;

Post::Post(unsigned int postId, string userName, string postText) : postId(postId), userName(userName), postText(postText) {
    if (postId == 0 || userName == "" || postText == "") {
        throw std::invalid_argument("post constructor: invalid parameter values");
    }
}

unsigned int Post::getPostId() {
    return postId;
}

string Post::getPostUser() {
    return userName;
}

string Post::getPostText() {
    return postText;
}

vector<string> Post::findTags() {
    // TODO: extracts candidate tags based on occurrences of # in the post
    vector<string> tags;
    stringstream ss(postText); //from zybookss
    string text = "";

    while (ss >> text) {

        if (text[0] != '#') {
            continue; //if the first item in every word is not a # keep going
        }
        for (size_t i = 1; i < text.size(); i++) {
            if (isalpha(text[i])) {
                text.at(i) = tolower(text.at(i)); 
            }
            else if ((text.at(i) == '!') || (text.at(i) == ',') || (text.at(i) == '.') || (text.at(i) == '?')) {
                text.pop_back();
            }
        }
        tags.push_back(text);
    }
    return tags;
}
