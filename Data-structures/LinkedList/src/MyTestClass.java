import java.util.Collections;
// test class for public class SinglyLinkedList <T extends Comparable<T>> 
//implements List<T>
public class MyTestClass {
	
	public static void main(String[] args) {
		
		List<Integer> List1, List2;
		List1 = new SinglyLinkedList<Integer>();
		List2 = new SinglyLinkedList<Integer>();
		List1.addAtHead(1);
		System.out.println("List1 after adding integer 1 at head " + List1);
		List1.addAtEnd(0);
		List1.addAtHead(2);
		System.out.println("List1 after adding integer 0 at head and 2 at end is " +List1);
		System.out.println("List size is "+ List1.size());
		System.out.println("List1 value at index 1 is " +List1.get(1));
		System.out.println("0 in List1 is at index" +List1.indexOf(0));
		List1.add(1,5);
		List1.addAtHead(-5);
		System.out.println("List 1 after adding 5 at index 1 " + List1);
		System.out.println("List1 after removing object at index 2 "+List1.remove(2));
		System.out.println("List1 after removing at head " + List1);
		System.out.println("Smallest value is "+List1.min());
		System.out.println("Smallest value is "+List1.minR());
		System.out.println("Largest value is "+List1.max());
		System.out.println("Largest value is "+List1.maxR());
		System.out.println("List2 being empty is " + List2.Empty()) ;
		List1.replace(-5,3);
		List1.addAtHead(1);
		System.out.println("New list after replacing -5 with 3 is " + List1);
		List2 = List1.duplicate(3);
		System.out.println("List 1 duplicating 1 item " + List1.duplicate(1));
		System.out.print("List 1 printed reverse is ");
		List1.reverse();
		System.out.println("List of all elements in List 1 greater than 2 is " + List1.countGreaterThan(1));
		System.out.println("List 1 equals List 2 is " + List1.equals(List2));
		List2 = List1;
		System.out.println("List 1 equals List 2 after List2=List1 is " + List1.equals(List2));
		System.out.print("List 1 after remove even is ");
		List1.removeEven();
		System.out.println("After removing even indexes "+ List1);
		
	}	

}
