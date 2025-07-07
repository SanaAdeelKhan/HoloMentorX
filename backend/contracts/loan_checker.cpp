int checkEligibility(int income, int creditScore) {
    if (income >= 50000 && creditScore >= 700) {
        return 1;
    } else {
        return 0;
    }
}
