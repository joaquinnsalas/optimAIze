// These headers define some of the classes and functions we need
#include <iostream>
#include <string>
#include <sstream>
#include <limits>

// ONLY MAKE CHANGES WHERE THERE IS A TODO

// These using declarations let us refer to things more simply
// e.g. instead of "std::cin" we can just write "cin"
using std::cin, std::cout, std::endl;
using std::string, std::getline;

// These methods are defined below the main function

// print instructions for inputting grades
void print_instructions();

// pretty print a summary of the grades
void print_results(double exam_average,
                   double hw_average,
                   double lw_average,
                   double reading,
                   double engagement,
                   double weighted_total,
                   char final_letter_grade);

// YOU ARE NOT EXPECTED TO UNDERSTAND THIS ONE... YET
// extract the category and score from the line
// and store the values in the provided variables
// if line := "exam 95", then category := "exam" and score := 95
// if the line is invalid, then category := "ignore"
void get_category_and_score(const string& line,
                            string* category,
                            double* score);

int main() {
    print_instructions();

    // ONLY MAKE CHANGES WHERE THERE IS A TODO

    // TODO(student): declare and initialize variables that you want
    //Variables were declared here
    double totalexam = 0.0;
    double totalfinal = 0.0;
    double totalhw = 0.0, numofhw = 0.0;
    double totallw = 0.0, numoflw = 0.0;
    double totalread = 0.0, numofread = 0.0;
    double totalengagement = 0.0, numofengagement = 0.0;
    double totprogcheck = 0.0;
    double tot_exam_average = 0.0;

    string line;
    // read one line from standard input (discards the ending newline character)
    getline(cin, line);
    // read lines until an empty line is read
    while (!line.empty()) {
        string category;
        double score;
        get_category_and_score(line, &category, &score);

        // process the grade entry
        if (category == "exam") {
            // TODO(student): process exam score
            totalexam += score; //adds up all of exam grades

        } else if (category == "final-exam") {
            totalfinal += score; //adds up all final exam grades
            // TODO(student): process final score

        } else if (category == "hw") {
            // TODO(student): process hw score
            totalhw += score; //adds up all of homework grades
            numofhw++; //counts how many homeworks there are

        } else if (category == "lw") {
            // TODO(student): process lw score
            if (score != 0){ 
                score = 100; //sets '1' == '100'
            }else {
                score = 0; //sets '0' == '0'
            }
            totallw += score; //adds up lw grades
            numoflw++; //counts how many labworks

        } else if (category == "reading") {
            // TODO(student): process reading score
            totalread += score;
            numofread++;

        } else if (category == "engagement") {
            // TODO(student): process engagement score
            totalengagement += score;
            numofengagement++;

        }else if  (category == "program-check") {
            // TODO(student): process program-check score
            totprogcheck += score;

        }else {
            cout << "ignored invalid input" << endl;
        }

        // get the next line from standard input
        getline(cin, line);
    }

    // TODO(student): compute component averages
    double exam_average = 0;
    tot_exam_average = ((totalexam + totalfinal) / (3));
    
    double hw_average = 0;
    if (numofhw != 0){
        hw_average = (totalhw / numofhw);
    }
    double lw_average = 0;
    if (numoflw != 0){
        lw_average = ((totallw) / (numoflw)) * (0.5 + (totprogcheck / 4));
    }
    double reading = 0.0;
    if(numofread != 0){
        reading = ((totalread / numofread) + 15);
    }else{
        reading += 15;
    }
    if(reading > 100 ){
        reading = 100;
    }
    double engagement = 0;
    if (numofengagement != 0){
        engagement = ((totalengagement / numofengagement) + 15);
    }else{
        engagement += 15;
    }
    if (engagement > 100){
        engagement = 100;
    }

    // TODO(student): compute weighted total of components
    //This chooses either the average of the 3 exams OR the
    //final exam grade depending on which grade is higher
    double weighted_total = 0;
    if (totalfinal >= tot_exam_average){
        exam_average = totalfinal;
    }
    else{
        exam_average = tot_exam_average;
    }
    weighted_total = (hw_average * 0.40) + (lw_average * 0.10) + (exam_average * 0.40) + (reading * 0.05) + (engagement * 0.05);

    // TODO(student): compute final letter grade
    //Sets ranges that decide what the grade is 
    char final_letter_grade = 'j'; {
    if (weighted_total >= 90.0) final_letter_grade = 'A';
    else if (weighted_total >= 80.0) final_letter_grade = 'B';
    else if (weighted_total >= 70.0) final_letter_grade = 'C';
    else if (weighted_total >= 60.0) final_letter_grade = 'D';
    else final_letter_grade = 'F';
    }

    print_results(
        exam_average, hw_average, lw_average, reading, engagement,
        weighted_total, final_letter_grade);
}

// These methods are already implemented for you
// You should not need to modify them

void print_instructions() {
    cout << "enter grades as <category> <score>" << endl;
    cout << "  <category> := exam | final-exam | hw | lw | reading | engagement | program-check" << endl;
    cout << "     <score> := numeric value" << endl;
    cout << "enter an empty line to end input" << endl;
}

void get_category_and_score(
    const string& line,
    string* category,
    double* score) {
    // turn the string into an input stream
    std::istringstream sin(line);

    // read the category (as string) and score (as double) from the stream
    sin >> *category;
    sin >> *score;

    if (sin.fail()) {
        // the stream is in a fail state (something went wrong)
        // clear the flags
        sin.clear();
        // clear the stream buffer (throw away whatever garbage is in there)
        sin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        // signal that the line was invalid
        *category = "ignore";
    }
}

void print_results(
    double exam_average,
    double hw_average,
    double lw_average,
    double reading,
    double engagement,
    double weighted_total,
    char final_letter_grade) {
    cout << "summary:" << endl;
    cout << "      exam average: " << exam_average << endl;
    cout << "        hw average: " << hw_average << endl;
    cout << "        lw average: " << lw_average << endl;
    cout << "           reading: " << reading << endl;
    cout << "        engagement: " << engagement << endl;
    cout << "    ---------------" << endl;

    cout << "    weighted total: " << weighted_total << endl;

    cout << "final letter grade: " << final_letter_grade << endl;
}
