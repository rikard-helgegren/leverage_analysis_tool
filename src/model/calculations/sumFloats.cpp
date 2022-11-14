
float sumFloats(float* floatArray, int nrOfFloats){
    float sum = 0.0f;

    for (int i =0; i< nrOfFloats; i++){
        sum = sum + floatArray[i];
    }

    return sum;
}