
public class QuestionOne {
	
	public static void main (String[] args) {
		
			ArrayStack<Integer> k = new ArrayStack<Integer>(20);
			for (int i = 0; i < 21; i++) {
				k.push(i);
			}
			
			k.display();
			k.reverse();
			k.display();
			k.peek();
			k.pop();
			k.pop();
			k.reverse();
			k.size();
			k.isFull();
			k.isEmpty();
			k.display();
			k.clear();
			k.display();
			k.isEmpty();
			
	}

	

}
