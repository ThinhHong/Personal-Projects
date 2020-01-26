
public interface Stack<T> {
	
	
	public abstract boolean isEmpty();
	public abstract boolean isFull();
	public abstract T peek();
	public abstract T pop();
	public abstract void push( T element );
	public abstract void clear();
	
}

