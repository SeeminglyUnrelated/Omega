# include <string>
# include <iostream>

class Token
{
public:
    std::string INT = "INT";
    std::string STR = "STR";
    std::string PLUS  = "PLUS";
    std::string MINUS = "MINUS";
    std::string MUL   = "MUL";
    std::string DIV   = "DIV";

    Token(std::string atype, int value = NULL);
    ~Token();
}

Token::Token(std::string atype, int value)
{
    std::string type = atype;
    int value = value;
}

Token::~Token()
{}

int main(){
    std::cout << "test";
    return 0;
}