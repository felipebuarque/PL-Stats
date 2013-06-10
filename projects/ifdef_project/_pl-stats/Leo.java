
public class Leo {

	public Leo(){
		
	}
	
	public void leoEhFoda(int x, String texto[]) {
		
		//#ifdef FeatureA
			
		//#endif
		
		//#ifndef FeatureB
			private int y;
		//#endif
		
		//#ifdef FeatureC
			
			//#ifdef FeatureD
				y = x;
			//#endif
		
		//#endif
		
		//#ifdef FeatureE
		for(int i = 0; i < 10; i++){
			if(i == 4){
				break;
			} else {
				continue;
			}
		}
		//#endif
		
		//#ifdef FeatureF
		
		//#elif FeatureG
		
		//#else
		
		//#endif
		
		//#mdebug debug1
		
		//#enddebug
		
		//#mdebug debug2
		
		//#enddebug
		return x;
		
	}
	
	public void leoEhFoda2() {
		
		private int x, y, z;
		private String texto = 'opa';
		
		X.z = 'teste';
		
		if(z == 'teste'){
//			#ifdef FeatureSpecial
			z = 'outro teste'
//			#endif
		}
		
		//#mdebug debug3
		y = 1;
		for(int i = 0; i < sizeof(x); i++){
			z = "texto1";
		}
		//#enddebug
		
		//#mdebug debug4
		while(x = 1){
			x++;
		}
		//#enddebug
		
		//#ifndef FeatureH || FeatureH2
		x = 2;
		leoEhFoda(x);
		//#elifndef FeatureI
		y = Y.x;
		y = leoEhFoda(x, y);
		//#else
		texto = "texto aqui!";
		//#endif
	}
	
}
