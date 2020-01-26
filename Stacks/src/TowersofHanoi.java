
public class TowersofHanoi {
	
	private ArrayStack<Integer>[] rods;

	
	public TowersofHanoi( int n) {
		
		rods = (ArrayStack<Integer>[]) new ArrayStack[3];
		rods[0] = new ArrayStack<Integer>(n);
		for (int i = n; i > 0; i--) {
			rods[0].push(i);
		}
		rods[1] = new ArrayStack<Integer>(n);
		rods[2] = new ArrayStack<Integer>(n);
		
	}
	
	public boolean legalMove(int a, int b) {
		
		boolean flag = false;
		if (rods[b].isEmpty()){
			
			return true;	
		}
		
		if ((!rods[a].isEmpty()) && (!rods[b].isEmpty())) {
			
			if (rods[a].peek() < rods[b].peek()) {
				
				flag = true;	
		}
		
		}
		return flag;
		
	}
	
	public boolean move(int a, int b) {
		
		String move ="";
		if (! legalMove(a,b)) {
			return false;
		}
		
		move = move + "disc" + rods[a].peek() + " moved from rod" + a + " to rod" + b;
		System.out.println(move);
		int x = rods[a].pop();
		rods[b].push(x);
		return true;
	}
	
	public boolean move (int m, int a, int b, int c) {
		
		
		
		for (int i = 0; i < m; i++) {
			
			if (! legalMove(a,b)) {
				return false;
			}
			int tmp = rods[a].pop();
			rods[c].push(tmp);
			if (! legalMove(a,c)) {
				return false;
			}
			tmp = rods[c].pop();
			rods[b].push(tmp);
			if (! legalMove(c,b)) {
				return false;
			}
			if (! rods[b].isEmpty()) {
				tmp = rods[b].pop();
				rods[c].push(tmp);
			}
	
		}
		return true;
		
	}
	
	public void showTowerStates() {
		System.out.println("First Tower = " + rods[0]);
		System.out.println("Second Tower = " + rods[1]);
		System.out.println("Third Tower = " + rods[2]);
	}
	
	public void solveGame() {
		
		
	}
}