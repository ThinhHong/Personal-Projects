
public class ArrayStack<T> implements Stack<T> {

    private T[] elems;
    private int top;    
    
    public ArrayStack( int cap ) {
        elems = (T[]) new Object[cap];
        top = 0;
    }

    // Returns true if this ArrayStack is empty

    public boolean isEmpty() {

        // Same as:
        // if ( top == 0 ) {
        //     return true;
        // } else {
        //     return false;
        // }
    
        return ( top == 0 );
    }

    // Returns the top element of this ArrayStack without removing it
    
    public boolean isFull() {
    	
    	return top == elems.length;
    }

    public T peek() {

        // pre-conditions: ! isEmpty()

        return elems[ top-1 ];
    }

    // Removes and returns the top element of this stack

    public T pop() {

        // pre-conditions: ! isEmpty()
        
        // *first* decrements top, then access the value!
        T saved = elems[ --top ];

        elems[ top ] = null; // scrub the memory!

        return saved;
    }

    // Puts the element onto the top of this stack.

    public void push( T element ) {

        // Pre-condition: the stack is not full

        // *first* stores the element at position top, then increments top
       if(element!=null &&top<elems.length ){
         elems[ top] = element; 
         top++;
       }
        
    }
    public void clear() {
    	
    	for (int i = 0; i< top; i++) {
    		elems[i] = null;
    	}
    }
    
   public int size() {
	   
	   return elems.length;
   }
   
   public void reverse() {
	 
	   T[] tmp = elems;
	   for (int i = 0; i <elems.length;i ++) {
		   
		   tmp[i] = elems[i];
		   System.out.println(tmp[i]);
	   }
	   
	   for (int i = 0; i < elems.length;i++) {
		   T saved = tmp[i];
		   System.out.println(saved);
		   elems[elems.length - i - 1] = saved;
	   }
      
   }
   
   public String toString() {
	   
	   String Tmp = "Stack contains [";
	   for (int i = 0; i < top ; i++) {
		   Tmp = Tmp + elems[i] + ", ";
	   }
	   Tmp = Tmp + "]";
	   return Tmp;
   }
   public void display() {
	   
	   String Tmp = "Stack contains [";
	   for (int i = 0; i < top ; i++) {
		   Tmp = Tmp + elems[i] + ", ";
	   }
	   Tmp = Tmp + "]";
	   System.out.println(Tmp);
	   
   }
}
    
