import java.util.Collections;
import java.util.Comparator;
public class SinglyLinkedList <T extends Comparable<T>> implements List<T>{
	
	// private class creates a node with a generic value pointing towards another node
	private static class Node<T> {
        private T value;
        private Node<T> next;
        private Node(T value, Node<T> next ) {
            this.value = value;
            this.next = next;
        }
    }

	// instance variable
    private Node<T> head;
    
    // Constructor and points head to null
    public SinglyLinkedList() {
    	
        head = null;
    }


    public void addAtHead(T item) {
    	
    	if(item == null) {
            throw new NullPointerException("Must not be of type null");
        }
        head = new Node<T>( item, head );
    }
    
    public void addAtEnd(T item) {
    	
    	if(item == null) {
            throw new NullPointerException("Must not be of type null");
        }
    	Node<T> newNode = new Node<T>(item,null);
    	if (head == null) {
    		head = newNode;	
    	}
    	else {
    		Node<T> l = head;
    		while(l.next != null) {
    			l = l.next;
    		}
    		l.next = newNode;

    	}
 
    }
    
    public boolean Empty() {
    	return head == null;
    }
    
    public int size() {
        
    	return size(head);
    }
    private int size(Node<T> k) {
    	
    	int size;
    	if (k == null) {
    		return 0;
    	}
    	else {
    		
    		size = 1 + size(k.next);
    	}
    	return size;
    }
    
    public T get(int i) {
    	if (i < 0) {
    		throw new IndexOutOfBoundsException("index not in range");
    	}
    	if (i > size()) {
    		throw new IndexOutOfBoundsException("index not in range");
    	}
    	return get(i,head);
    }
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to find value at index i
    private T get(int i,Node<T> k) {

    	if (k == null) {
    		return null;
    	}
    	if (i == 0) {
    		return k.value;
    	}
    	return get(i-1, k.next);
 
    	
    }
    
    public int indexOf(Object item) {
    	
    	return indexOf(item,head);
    }
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to return index of a certain item
    private int indexOf(Object item,Node<T> k) {
    	
    	if (k == null) {
    		return -1;
    	}
    	if (k.value.equals(item)) {
    		return 0;
    	}
    	int res = indexOf(item,k.next);
    	if (res == -1) {
    		return res;
    	}
    	
    	return res+1;
    }
    public void add(int i, T item) {
    	
    	if (i < 0) {
    		throw new IndexOutOfBoundsException("index not in range");
    	}
    	if (i > size()) {
    		throw new IndexOutOfBoundsException("index not in range");
    	}
    	Node<T> k = head;
    	if (i == 0) {
    		addAtHead(item);
    	}
    	else {
    		for (int j = 0; j < i - 1; j++) {
    			k = k.next;
    		}
    		Node<T> newNode = new Node<T>(item,k.next);
    		k.next = newNode;
    		
    	}
    }
    
    public T remove(int i) {
    	
    	if (i < 0) {
    		throw new IndexOutOfBoundsException("index not in range");
    	}
    	if (i > size()) {
    		throw new IndexOutOfBoundsException("index not in range");
    	} 	
    	if (head == null) {
    		return null;
    	}
    	T saved;
    	if (i == 0) {
    		saved = head.value;
    		head = head.next;
    	}
    	Node<T> k = head;
    	for (int j = 0; j < i - 1; j++) {
			k = k.next;
		}
    	saved = k.next.value;
    	k.next = k.next.next;
    	return saved;
    }
    
    public T min() {
    	
    	if (head == null) {
    		return null;
    	}
    	T low;
    	low = head.value;
    	Node<T> k = head;
    	for (int i = 0; i < size(); i++) {
    		if(k.value.compareTo(low) < 0) {
    			low = k.value;    			
    		}
    		k = k.next;
    	}
    	return low;
    }
    
    public T minR() {
    	
    	if (head == null) {
    		return null;
    	}
    	return minR(head);
    }
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to return smallest value in List
    private T minR(Node<T> k) {
    	
    	T low;
    	if(k.next == null) {
    		
    		return k.value;
    	}
    	else {
    		low = minR(k.next);
    		if(k.value.compareTo(low) < 0) {
    			return k.value;
    		}
    		else {
    			return low;
    		
    		}
    	}
    }
    
    public T max() {
    	
    	if (head == null) {
    		return null;
    	}
    	T high;
    	high = head.value;
    	Node<T> k = head;
    	for (int i = 0; i < size(); i++) {
    		if(k.value.compareTo(high) > 0) {
    			high = k.value;    			
    		}
    		k = k.next;
    	}
    	return high;
    }
    
    public T maxR() {
    	
    	if (head == null) {
    		return null;
    	}
    	return maxR(head);
    }
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to return largest value in List
    private T maxR(Node<T> k) {
    	
    	T high;
    	if(k.next == null) {
    		
    		return k.value;
    	}
    	else {
    		high = maxR(k.next);
    		
    		if(k.value.compareTo(high) > 0) {
    			return k.value;
    	}
    		else {
    			return high;
    		}
    	}
    }
    
    public void replace(T item, T second) {
    	
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	int pos;
    	pos = indexOf(item);
    	Node<T> k = head;
    	if (pos == -1) {
    		System.out.println("Not in list");
    	}
    	else {
    		if (pos == 0){
    			Node<T> rNode = new Node<T>(second,k.next);
    			head = rNode;
    		}
    		for (int i = 0; i < pos - 1; i++) {
    			k = k.next;
    		}
    		Node<T> rNode = new Node<T>(second,k.next.next);
    		k.next = rNode;
    	}
    }
    
    public List<T> duplicate(T item){
    	
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	
    	return duplicate(item,head);	
    }
    
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to find smallest value in List
    private List<T> duplicate(T item, Node<T> k){
    	
    	List<T> dup;
    	if (k.next == null) {
    		dup = new SinglyLinkedList<T>();
    		if (k.value.compareTo(item) == 0 ) {
    			dup.addAtHead(k.value);
    			dup.addAtHead(k.value);
    		}
    		else {
    			dup.addAtHead(k.value);
    		}		
    	}
    	else {
    		
    		dup = duplicate(item,k.next);{
    			if (k.value.compareTo(item) == 0 ) {
        			dup.addAtHead(k.value);
        			dup.addAtHead(k.value);
        		}
        		else {
        			dup.addAtHead(k.value);
        		}
    		}
    	}
    	return dup;
    }
    
    public List<T> countGreaterThan(T threshold){
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	
    	return countGreaterThan(threshold, head);
    }
    
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to return a list that contains all elements larger than the threshold
    private List<T> countGreaterThan(T thershold , Node<T> k){
    	
    	List<T> greater;
    	if (k.next == null) {
    		greater = new SinglyLinkedList<T>();
    		if(k.value.compareTo(thershold) > 0) {
    			greater.addAtHead(k.value);
    		}
    	}
    	else {
    		greater = countGreaterThan(thershold,k.next);
    		if(k.value.compareTo(thershold) > 0) {
    			greater.addAtHead(k.value);
    		}
    	}
    	
    	return greater;
    }
    
    public void reverse() {
    	
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	reverse(head);
    }
    
    // private method called by class of same name uses an extra parameter Node<T> k 
    // to print all values in list in reverse order
    private void reverse(Node<T> k) {
    	
    	
    	if (k.next == null) {
    		System.out.print(k.value + ",");
    	}
    	else {
    		 reverse(k.next);
    		 if(k == head) {
    			 System.out.println(k.value);
    		 }
    		 else {
    			 System.out.print(k.value +",");
    		 }
  
    	}
    }
    
    public boolean equals(SinglyLinkedList<T> other) {
    	
    	if (head == null || other.head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	if(other.size() != size()) {
    		return false;
    	}
    	return equals(head,other.head);
    }
    private boolean equals(Node<T> other, Node<T> k) {
    	
    
    	if ( other == null && k == null) {
    		return true;
    	}
    	else { 
    		if (other.value.compareTo(k.value) == 0) {
    			return equals(other.next,k.next);
    		}
    		else {
    			return false;
    		}	
    	}
    }
    
    public int compareTo(T item,Node<T> k) {
    	return item.compareTo(k.value);
    }
    
   
    public List<T> inOrder(){
    	
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	List<T> order = new SinglyLinkedList<T>();
    	
    	return order;
    }
    
    public void removeEven() {
    	if (head == null) {
    		throw new IllegalStateException("The list is empty");
    	}
    	for (int i = 0; i < size();i++) {
    		if ((i%2) == 0) {
    			remove(i);
    		}
    	}
    }
   
    public String toString() {
    	
    	String List;
    	List = "";
    	if (head == null) {
    		List = "";
    	}
    	else {
    		Node<T> k = head;
        	for(int i = 0; i < size(); i++) {
        		List = List + k.value +",";
        		k = k.next;
        	}
    	}
    	return List;
    }
}