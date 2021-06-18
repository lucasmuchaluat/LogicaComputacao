int soma(int x, int y)
{
    int a;
    a = x + y;
    println(a);
    return a;
}

int fatorial(int x)
{
    if (x < 0)
    {
        return -1;
    }
    if (x == 0 || x == 1)
    {
        return 1;
    }
    return x * fatorial(x - 1);
}

int main()
{
    int a;
    int b;
    a = 3;
    b = soma(a, 4);
    println(a);
    println(b);
    println(fatorial(3));
}
