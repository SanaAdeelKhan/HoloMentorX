int canPurchase(int age, int quantity) {
    if (age < 18 && quantity > 2) return 0;
    return 1;
}
