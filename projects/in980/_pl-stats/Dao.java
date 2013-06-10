package in980.rgms.persistence;

import in980.rgms.utils.HibernateUtils;

import java.util.List;

import org.hibernate.Session;

public abstract class Dao<T>{
	
	//Session currentSession;

	public void inserir(T object) throws Exception{
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
		try {
//			s.beginTransaction();
			s.save(object);
//			s.getTransaction().commit();
		} catch (Exception e) {
//			s.getTransaction().rollback();
			e.printStackTrace();
			throw new Exception(e);
		}	
	}
	public void atualizar(T object) throws Exception{
		Session s = HibernateUtils.getSessionFactory().getCurrentSession();
		try {			
//			s.beginTransaction();
			s.update(object);
//			s.getTransaction().commit();
		} catch (Exception e) {
//			s.getTransaction().rollback();
			e.printStackTrace();
			throw new Exception(e);
		}
	}
	
	public void excluir(T object) throws Exception{
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
		try {
//			s.beginTransaction();		
			s.delete(object);		
//			s.getTransaction().commit();
		} catch (Exception e) {
//			s.getTransaction().rollback();
			e.printStackTrace();
			throw new Exception(e);
		}
	}
	
	@SuppressWarnings("unchecked")
	public List<T> listaTodos(){
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
//		s.beginTransaction();
		List<T> membros = s.createQuery("from " + getTabela()).list();
//		s.getTransaction().commit();
		return membros;		
	}
	
	@SuppressWarnings("unchecked")
	public T buscaPeloId(Integer id) throws Exception {		
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
//		s.beginTransaction();
		T object = (T) s.get(getTipoClasse(), id);
//		s.getTransaction().commit();
		return object;		
	}
	
	public List<T> buscar(T object) throws Exception {
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
//		s.beginTransaction();
		List<T> listaRetorno = montaLista(object, s);	
//		s.getTransaction().commit();
		return listaRetorno;
	}
	
	
	@SuppressWarnings("unchecked")
	protected abstract Class getTipoClasse();
	protected abstract String getTabela();
	protected abstract List<T> montaLista(T object, Session s);
	
}
