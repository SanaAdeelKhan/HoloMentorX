int predictGrade(int score) {
    if (score >= 90) return 4;
    else if (score >= 80) return 3;
    else if (score >= 70) return 2;
    else if (score >= 60) return 1;
    else return 0;
}
