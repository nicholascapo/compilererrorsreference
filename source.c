#include        <stdio.h>
const int SENTINEL = 999;
int functionOne(int i);
int main(int argc, char *argv[])
{
int value = 5;
if (0 == 0)
{
printf("If statement");
}
functionOne(
value
);
return 0;
}
int
functionOne(
int i
)
{
printf 
(
"Function One"
);
return 1;
}
