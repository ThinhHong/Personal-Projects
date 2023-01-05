
public class MyCalculator {
	
	public static Boolean isBalanced(String expression) {
		
		ArrayStack<Character> stack = new ArrayStack<Character>(100);
		char t = expression.charAt(0);
		if ((t == ']') ||(t == '>') ||(t == '}') ||(t == ')')) {
			
			System.out.println("Error");
			return false;	
			
		}
		
		if (t == '[') {
			
			stack.push(']');
		}
		else if(t == '<') {
			
			stack.push('>');
		}
		else if(t == '{') {
			
			stack.push('}');
			
		}
		else if(t == '(') {
			
			stack.push(')');

		}
		for (int i = 1; i < expression.length(); i++) {
			char c = expression.charAt(i);
			
			
			if (c == '[') {
				
				stack.push(']');
			}
			else if(c == '<') {
				
				stack.push('>');
			}
			else if(c == '{') {
				
				stack.push('}');
				
			}
			else if(c == '(') {
				
				stack.push(')');

			}
			else if(c == ']'){
				
				if (stack.isEmpty() == true) {
					return false;
				}
				
				if ( c == stack.peek()) {
					stack.pop();	
				}
				
				else if (c != stack.peek()){
					System.out.println("Error");
					return false;
				}
			}
			else if(c == '>'){
				
				if (stack.isEmpty() == true) {
					return false;
				}
				if ( c == stack.peek()) {
					stack.pop();	
				}
				
				else if (c != stack.peek()){
					System.out.println("Error");
					return false;
				}
			}
			else if(c == '}'){
				
				if (stack.isEmpty() == true) {
					return false;
				}
				if ( c == stack.peek()) {
					stack.pop();	
				}
				
				else if (c != stack.peek()){
					System.out.println("Error");
					return false;
				}
			}
			else if(c == ')'){
				
				if (stack.isEmpty() == true) {
					return false;
				}
				if ( c == stack.peek()) {
					stack.pop();	
				}
				
				else if (c != stack.peek()){
					System.out.println("Error");
					return false;
				}
			}	
			
		}
			if (stack.isEmpty() == true) {
				return true;
			}
		return false;
	}
	
	public static String infixToPostfix(String infix) {
		
		if (! isBalanced(infix)) {
			
			return "Error";
			
		}
		String Postfix;
		Postfix = "";
		ArrayStack<Character> operator = new ArrayStack<Character>(100);
		
		for (int i = 0; i < infix.length(); i++) {

			char c = infix.charAt(i);
			if ((c == '*') || (c== '/') ||(c =='(') || (c == '{') || (c == '[')||(c == '+') || (c== '-')) {
			operator.push(c);
	
			}
			else if ((c == ')') || (c == ']')||(c == '>') || (c== '}')){
				
				char t = operator.pop();
				Postfix = Postfix + t + " ";
				while ((t !='(') && (t != '{') && (t != '[')) {
					t = operator.pop();
				}				
			}
			else if (Character.isDigit(c)){
				
				Postfix = Postfix + c;
				if (i != infix.length() -1 ) {
				
					if(! Character.isDigit(infix.charAt(i+1))){
						Postfix = Postfix + " ";
			
						
				}
		
				}
		}
	}
		while (! operator.isEmpty()) {
			char x = operator.pop();
			Postfix = Postfix + x + " ";
			
		}
		return Postfix;
	}
	
	
	public static double evaluate(String postfix) {
		
		ArrayStack<Double> operator = new ArrayStack<Double>(100);
		
		double x = 0;
		String doub = "";
		for (int i = 0; i < postfix.length(); i++) {
			
			char c = postfix.charAt(i);
			if (Character.isDigit(c)) {
				
				doub = Character.toString(c);
				
				double l = Double.parseDouble(doub);
				operator.push(l);
			
			}
			else if (c == ' '){
				doub = "";
			}
			else if ((c == '+') || (c== '-') ||(c == '*') || (c == '/')) {
				
				
				
				double r = operator.pop();
				double l = operator.pop();

				
				if ( c == '+') {
					
					x = r + l;
				}
				else if ( c == '-') {
					
					x = r - l;
				}
				else if ( c == '*') {
					
					x = r * l;
				}
				else if ( c == '/') {
					
					x = l / r ;
				}
				
	
				operator.push(x);
				
				
				
			}
		}
		return x;
	}
	public static void main(String [] args) {
		
		System.out.println(infixToPostfix("1+3+2/(5+6)"));
		System.out.println(evaluate("1 3 2 5 6 * + + + "));
				
	}


}
