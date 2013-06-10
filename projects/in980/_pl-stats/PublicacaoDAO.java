package in980.rgms.persistence;

import in980.rgms.domain.Publicacao;

import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;

public class PublicacaoDAO extends Dao<Publicacao>{

	@Override
	protected String getTabela() {
		return "Publicacao";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return Publicacao.class;
	}

	@SuppressWarnings("unchecked")
	@Override
	protected List<Publicacao> montaLista(Publicacao object,
			Session s) {
		
		StringBuilder sb = new StringBuilder();	
		
		sb.append(" from Publicacao t where 0 = 0 ");
		
		String strQuery = montaQueryString(sb, object); 
		
		Query q = s.createQuery(strQuery);
		
		montaQuery(object, q);		
		
		List<Publicacao> listaRetorno = q.list();
		return listaRetorno;
	}

	/**
	 * Hook Method, usado para auxiliar na implementacao com AspectJ 
	 * @see in980.rgms.persistence.aspect.ListaPublicacaoPorNomeAspect 
	 * @see in980.rgms.persistence.aspect.ListaPublicacaoPorAnoAspect
	 * @param object
	 * @param q
	 */
	private void montaQuery(Publicacao object, Query q) {		
	}
	
	
	private String montaQueryString(StringBuilder sb, Publicacao p) {
		return sb.toString();		
	}
	
	
}
