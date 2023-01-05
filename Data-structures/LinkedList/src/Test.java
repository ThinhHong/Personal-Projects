
public class Test {
	
	// public method that takes the sum of all odd values in an int[] using recursion
	public static int sumOdd(int[] t) {
			
		if (t.length == 0){
			return 0;
		}
		else {
			return sumOdd(t,0);
		}
	}
	// private method that takes the sum of all odd values in an int[] using recursion
	// that uses an extra parameter to find inde
	private static int sumOdd(int[] t, int i) {
		
		if (i == t.length - 1) {
			if(t[i]%2 == 1) {
				return t[i];
			}
			return 0;
		}
		else {
			if(t[i]%2 == 1) {
				return(t[i] + sumOdd(t,i + 1));
			}
			else {
				return sumOdd(t,i+1);
			}
		}
	}
	
	// public method that finds the last occureance of an item in an int[] using recursion
	// has parameter t = to a int[] and n which is the target we are finding for
	public static int lastOccureance(int[] t,int n) {
		
		if (t.length == 0){
			return 0;
		}
		else {
			return lastOccureance(t,n,0);
		} 
	}
	// private method that finds the last occureance in an int[] using recursion that is called 
	// by the public method. Has an extra parameter to determine the index of an array
	private static int lastOccureance(int[] t, int n, int i) {
		
		int last;
		if(i == t.length -1) {
			if (t[i] == n) {
				return i;
			}
		}
		if(t[i] == n) {
			last = i;
			last = lastOccureance(t,n,i+1);
		}
		else {
			last = lastOccureance(t,n,i+1);
		}
		return last;
	}
	// takes in an array and finds a set of numbers in t that are == value and returns
	// an array with those numbers
	public static int[] sumArray(int[] t, int value){
		
		if (t.length == 0) {
			return null;
		}
		return sumArray(t,value,0);
		
	}
	// private method of sumArray that takes an extra parameter for the index of an array
	private static int[] sumArray(int [] t, int value, int index) {
		int[] array = new int[10];
		return array;
	}
	// Test area for Test.java arrays
	public static void main(String[] args) {
		int[] Array1,Array2;
		Array1 = new int[6];
		Array2 = new int[6];
		for (int i = 0;i<6;i++) {
			Array1[i]=i;
		}
		Array1[2] = 5;
		System.out.println("Sum of all odd indexes in Array 1 is " + sumOdd(Array1));
		System.out.println(lastOccureance(Array1,5));

	}
}


