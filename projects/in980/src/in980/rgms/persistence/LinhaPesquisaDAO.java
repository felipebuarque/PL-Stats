package in980.rgms.persistence;

import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.TipoMembro;
import in980.rgms.utils.HibernateUtils;

import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;

public class LinhaPesquisaDAO extends Dao<LinhaPesquisa>{
	
	
	@SuppressWarnings("unchecked")
	protected List<LinhaPesquisa> montaLista(LinhaPesquisa object, Session s) {
		List<LinhaPesquisa> listaRetorno = s.createQuery("from " + getTabela()+ 
				" t where upper(t.descricao) like :descricao " )
			.setString("descricao", "%" + object.getDescricao().toUpperCase() + "%")
			.list();
		return listaRetorno;
	}

	@Override
	protected String getTabela() {
		return "LinhaPesquisa";
	}

	@SuppressWarnings("unchecked")
	@Override
	protected Class getTipoClasse() {
		return LinhaPesquisa.class;
	}
	
	@SuppressWarnings("unchecked")
	public List<LinhaPesquisa> getByMembro(Membro membro) {
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();		
		List<LinhaPesquisa> linhasPesquisa = s.createQuery(" from " + getTabela() + 
				" t where t.membros.id = :id_membro ").setInteger("id_membro", membro.getID()).list();		
		
		return linhasPesquisa; 
	}

}
