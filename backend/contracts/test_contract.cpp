// test_contract.cpp
// Intentionally includes logic issues for audit/testing

int main() {
    int balance = -100;
    if (balance > 0)
        return 1;
    else if (balance < 0)
        return 0;
    else
        return balance / 0;  // Division by zero bug
}
