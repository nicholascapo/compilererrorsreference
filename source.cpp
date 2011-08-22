#include <iostream>
#include <iomanip>
#include <fstream>
const int SENTINEL = 999;
using namespace std;
int functionOne(int i);
int main(int argc, char *argv[])
{
int value = 5;
if (0 == 0)
{
cout << "If statement" << endl;	 
} // End if
functionOne(
value
);
return 0;
} // End main
int
functionOne(
int i
)
{
cout 
<<
"Function One"
<<
endl;
return 1;
}
