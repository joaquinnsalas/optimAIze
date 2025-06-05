# include <string>
# include <stdexcept>
# include "Tag.h"

using std::string, std::vector;

Tag::Tag(string tagName) : tagName(tagName), tagPosts({}) /* TODO: initialize */ {
    // TODO: implement constructor checks
    size_t taglen = tagName.length();
    if (tagName.empty()) {
        throw std::invalid_argument("There is nothing here.");
    }
    else if (taglen < 2) {
        throw std::invalid_argument("No hashtag letters.");
    }
    else if (tagName[0] != '#') {
        throw std::invalid_argument("This is not a hashtag.");
    }
    else if (!isalpha(tagName[1])) {
        throw std::invalid_argument("First item has to be a letter");
    }
    else if (!isalpha(tagName.substr(taglen - 1)[0])) {
        throw std::invalid_argument("Bad Hashtag");
    }
    else if (!isalpha(tagName.substr(taglen - 2)[0])) {
        throw std::invalid_argument("Bad Hashtag");
    }
    for (size_t i = 1; i < tagName.size(); i++) { //check last
        if (!(islower(tagName.at(i)))) {
            throw std::invalid_argument("No uppercase words.");
        }
    }
    this->tagName = tagName;
}

string Tag::getTagName() {
    return tagName; // TODO: implement getter
}

vector<Post*>& Tag::getTagPosts() {
    return tagPosts; // TODO: implement getter
}

void Tag::addTagPost(Post* post) {
    if (post == nullptr) {
        throw std::invalid_argument("Null pointer");
    }
    tagPosts.push_back(post); // TODO: add post to tag posts
}
