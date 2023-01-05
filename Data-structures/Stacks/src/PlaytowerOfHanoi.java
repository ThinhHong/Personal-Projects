import java.util.Scanner;
public class PlaytowerOfHanoi {
	
	public static void main(String[] args)
	 { 
		
		 System.out.println("How many disk would you like to play with?");
		 Scanner Scan = new Scanner(System.in);
		 String answer =Scan.nextLine();
		 int x = Integer.parseInt(answer);
		 System.out.println("Would you like to play play a game or see a demo solution? ");
		 String expression=Scan.nextLine();
		 TowersofHanoi k = new TowersofHanoi(x);
		 k.showTowerStates();
		 if (expression == "play") {
			 
		 }
		 }
	 }



