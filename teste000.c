
/*Ok*/

int soma(int x, int y)
{
    int res;
    res = x + y;
    return res;
}

bool comparaSoma()
{
    bool res;
    int x;
    x = 3;

    res = soma(x, 2) == 8;

    return res;
}

int main()
{
    int x;
    bool z;

    z = comparaSoma();
    x = z;
    println(x);
}
