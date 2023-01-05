// interface List<T> using generics and extending the class Comparable
public interface List <T> {
	
	// returns the size of List node using recursion
	public abstract int size();
	// returns the element at position i using recursion
	public abstract T get(int i);
	// returns the index of item using recursion
	public abstract int indexOf(Object item);
	// adds a generic item at position i using recursion
	public abstract void add(int i,T item);
	// removes and returns a object at index i
	public abstract T remove(int i);
	// returns lowest value item
	public abstract T min();
	// returns lowest value item using recursion
	public abstract T minR();
	// returns highest value item
	public abstract T max();
	// returns highest value item using recursion
	public abstract T maxR();
	// returns if list is empty or not
	public abstract boolean Empty();
	// adds item at head of list
	public abstract void addAtHead(T item);
	// adds item at end of list
	public abstract void addAtEnd(T item);
	// searches for first elements and replaces it with the second
	public abstract void replace(T first, T second);
	// creates a list that duplicates every element == to item
	public abstract List<T> duplicate(T item);
	//  prints out data elements in reverse order using recursion
	public abstract void reverse();
	//ReturnsList of all elements greater than threshold
	public abstract List<T> countGreaterThan(T threshold);
	// returns true of other has the same elements in the list with the same order
	public abstract boolean equals(Object other);
	// returns a String showing all elements seperates by a comma
	public abstract String toString();
	// returns a new list that has all the elements in the list sorted in ascending order
	public abstract List<T> inOrder();
	// remove all elements at even positions
	public abstract void removeEven();
	
	
	
	

}
