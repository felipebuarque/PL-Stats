package in980.rgms.persistence.aspect;

import org.hibernate.Query;

import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.PublicacaoDAO;


public aspect ListaPublicacaoPorNomeAspect {
	//Pointcut
	pointcut searchByNameBefore(StringBuilder sb, Publicacao p): 
		call(private String PublicacaoDAO.montaQueryString(StringBuilder, Publicacao)) &&
		args(sb, p);
	
	pointcut searchByNameAfter(Publicacao p, Query q): 
		call(private void PublicacaoDAO.montaQuery(Publicacao, Query)) &&
		args(p, q);
	
	
	//Advice	
	before (StringBuilder sb, Publicacao p): searchByNameBefore(sb, p) {
		if(p.getTitulo() != null && !p.getTitulo().equals("")) {
			sb.append(" and  upper(t.titulo) like :titulo ");
		}
	}
	
	
	//Advice	
	after (Publicacao p, Query q): searchByNameAfter(p, q) {
		if(p.getTitulo() != null && !p.getTitulo().equals("")) {
			q.setString("titulo", "%" + p.getTitulo().toUpperCase() + "%");
		}
	}
}
