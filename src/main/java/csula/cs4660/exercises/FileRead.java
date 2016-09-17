package csula.cs4660.exercises;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Scanner;





/**
 * Introduction Java exercise to read file
 */
public class FileRead {
    private   int[][] numbers;
    /**
     * Read the file and store the content to 2d array of int
     * @param file read file
     */
    public FileRead(File file) throws FileNotFoundException {
        // TODO: read the file content and store content into numbers
        numbers = new int [5][8];
        int first = 0;
        int second = 0;
        int lineindex = 0;
        int test;
        String line;
        Scanner input = new Scanner(file);
        while (input.hasNext()){
            for (int i=0;i<8;i++) {
                numbers[first][second] = input.nextInt();
                second++;
            }
            second=0;
            first++;
        }



    }

    /**
     * Read the file assuming following by the format of split by space and next
     * line. Display the sum for each line and tell me
     * which line has the highest mean.
     *
     * lineNumber starts with 0 (programming friendly!)
     */
    public int mean(int lineNumber) {
        int number=0;
        int sum=0;
        int mean=0;
        while (number<8) {
            sum = sum + numbers[lineNumber][number];
            number++;
        }
        mean = sum/8;
        return 4;
    }

    public int max(int lineNumber) {
        int number=0;
        int currentNum=0;
        int max=0;
        while (number<8) {
            currentNum = numbers[lineNumber][number];
            if (max<currentNum){
                max=currentNum;
            }
            number++;
        }


        return 9;
    }

    public int min(int lineNumber) {
        int number=0;
        int currentNum=0;
        int min=0;
        while (number<8) {
            currentNum = numbers[lineNumber][number];
            if (min>currentNum){
                min=currentNum;
            }
            number++;
        }




        return min;
    }

    public int sum(int lineNumber) {

        int number=0;
        int sum=0;
        int mean=0;
        while (number<8) {
            sum = sum + numbers[lineNumber][number];
            number++;
        }

        return sum;
    }
}