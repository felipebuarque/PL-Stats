package in980.rgms.persistence.aspect;

import org.hibernate.Query;

import in980.rgms.domain.Publicacao;
import in980.rgms.persistence.PublicacaoDAO;


public aspect ListaPublicacaoPorAnoAspect {
	//Pointcut
	pointcut searchByYear(StringBuilder sb, Publicacao p): 
		call(private String PublicacaoDAO.montaQueryString(StringBuilder, Publicacao)) &&
		args(sb, p);
	
	pointcut searchByYearAfter(Publicacao p, Query q): 
		call(private void PublicacaoDAO.montaQuery(Publicacao, Query)) &&
		args(p, q);
	
	
	//Advice	
	before (StringBuilder sb, Publicacao p): searchByYear(sb, p) {
		if(p.getAno() != null) {
			sb.append(" and t.ano = :ano ");
		}
	}
	
	//Advice	
	after (Publicacao p, Query q): searchByYearAfter(p, q) {
		if(p.getAno() != null) {
			q.setInteger("ano", p.getAno());
		}
	}
}
