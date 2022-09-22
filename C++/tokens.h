# include <iostream>
# include <string>

using namespace std;
class Token{
    public:  
        string INT = "INT";
        string STR = "STR";
        string PLUS  = "PLUS";
        string MINUS = "MINUS";
        string MUL   = "MUL";
        string DIV   = "DIV";
        Token(string type, auto value);
        ~Token();
};