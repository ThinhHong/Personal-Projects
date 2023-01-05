
public class ListStack <T> implements Stack<T> {
	
	private Elem<T> top;
	private int cap;
	  private static class Elem<T>{
	    private T value;
	    private Elem<T> next;
	    private int cap;

	    
	    public Elem(T val, Elem<T> next){
		      this.value = val;
		      this.next= next;

		    }
		  
	    
	   public Elem(T val, Elem<T> next, int capacity){
	      this.value = val;
	      this.next= next;
	      this.cap = capacity;
	    }
	  }
	  
	   public  boolean isEmpty(){
	      return (top== null);
	    }
	   
	   public boolean isFull() {
		  
		   
		   return true;
		   
		   
	   }
	   
	  
	    public void push(T obj){
	      
	      top= new Elem<T>(obj,top);
	      
	    }
	    
	    public T pop(){
	      if(!isEmpty()){
	         T saved= top.value;
	        top=top.next;
	        return saved;
	      }
	      return null;
	    }
	     public T peek(){
	        if(!isEmpty()){
	          return top.value;
	     }
	       else return null;

	}
	     
	     public void clear() {
	    	 top = null;
	     }
	     
	     public int size() {
	    	 int size = 0;
	    	 Elem<T> tmp = top;
	    	 while( !isEmpty()) {
	    		 
	    		 T saved = tmp.value;
	    		 tmp = tmp.next;
	    		 size++;
	    	 }
	    	 tmp = null;
	    	 return size;
	    	 
	     }
	     
	     public int capacity() {
	    	 return cap;
	     }

	     public String toString() {
	    	 
	    	 String t = "[";
	    	 Elem<T> tmp = top;
	    	 for (int i = 0; i < size(); i++) {
	    		 t = t + tmp.value + tmp.next +", "; 
	    	 }
	    	 t = t + "]";
	    	 tmp = null;
	    	 return t;
	     }
	     
	     public void display() {
	    	 
	    	 String t = "[";
	    	 Elem<T> tmp = top;
	    	 for (int i = 0; i < size(); i++) {
	    		 t = t + tmp.value + tmp.next +", "; 
	    	 }
	    	 t = t + "]";
	    	 tmp = null;
	    	 System.out.println(t);
	    	 
	     }

}
