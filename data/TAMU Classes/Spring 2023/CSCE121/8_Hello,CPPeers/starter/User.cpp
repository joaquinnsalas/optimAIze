# include <string>
# include <iostream>
# include <stdexcept>
# include "User.h"

using std::string, std::vector;

User::User(string userName) : userName(userName), userPosts({}) /* TODO: initialize */ {
    // TODO: implement constructor checks
    if (userName.empty()) {
        throw std::invalid_argument("String is empty.");
    }
    if (!isalpha(userName[0])) {
        throw std::invalid_argument("First letter is not alphabet");
    }
    for (size_t i = 0; i < userName.size(); i++) {
        if (!(islower(userName[i]))) {
            throw std::invalid_argument("Uppercase letters");
        }
    }
    User::userName = userName;
}

string User::getUserName() {
    return userName; // TODO: implement getter
}

vector<Post*>& User::getUserPosts() {
    return userPosts; // TODO: implement getter
}

void User::addUserPost(Post* post) {
    if (post == nullptr) {
        throw std::invalid_argument("Nullpointer");
    }
    userPosts.push_back(post); // TODO: add post to user posts
}
