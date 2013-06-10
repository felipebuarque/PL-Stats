import in980.rgms.domain.ArtigoConferencia;
import in980.rgms.domain.ArtigoRevista;
import in980.rgms.domain.LinhaPesquisa;
import in980.rgms.domain.Membro;
import in980.rgms.domain.Publicacao;
import in980.rgms.utils.HibernateUtils;

import java.io.StringWriter;
import java.util.ArrayList;
import java.util.List;

import org.apache.velocity.Template;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;
import org.hibernate.Session;


public class Main {

	public static void main(String[] args) {
		try {
			new Main().testandoVelocity();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	private void testandoVelocity() throws Exception{
		Velocity.init();

        /* lets make a Context and put data into it */

        VelocityContext context = new VelocityContext();

        context.put("name", "Velocity");
        context.put("project", "Jakarta");

        /* lets render a template */

        StringWriter w = new StringWriter();
        
        Template template = Velocity.getTemplate("/home/leofernandesmo/workspace/IN980-ResearchGroupManagementSystem/src/testtemplate.vm");

        //Velocity.mergeTemplate("/home/leofernandesmo/workspace/IN980-ResearchGroupManagementSystem/src/testtemplate.vm", context, w );
        template.merge(context, w);
        System.out.println(" template : " + w );

        /* lets make our own string to render */

        String s = "We are using $project $name to render this.";
        w = new StringWriter();
        Velocity.evaluate( context, w, "mystring", s );
        System.out.println(" string : " + w );

	}

	private void teste() {
		Session s  = HibernateUtils.getSessionFactory().getCurrentSession();
		s.beginTransaction();
		
		Membro m = new Membro();
		m.setNome("Jose");
		m.setFone("9989897");
		m.setEmail("a@a");		
		s.save(m);		
		
		Publicacao p = new ArtigoConferencia();
		p.setTitulo("Titulo Teste 1");
		p.setAno(2009);
		List<Membro> membros = new ArrayList<Membro>();
		membros.add(m);
		p.setAutoresMembros(membros);
		s.save(p);
		
		ArtigoRevista ar = new ArtigoRevista();
		p.setTitulo("Titulo Teste 1");
		p.setAno(2009);
		p.setFilePath("/home/leofernandesmo/woorkspace/teste.jpg");
		s.save(ar);
		
		LinhaPesquisa lp = new LinhaPesquisa();
		lp.setTitulo("Linah Teste 1");
		lp.setDescricao("Descricao teste 1");
		List<Membro> membros1 = new ArrayList<Membro>();
		membros1.add(m);
		lp.setMembros(membros1);
		List<Publicacao> publicacoes = new ArrayList<Publicacao>();
		publicacoes.add(p);		
		lp.setPublicacoes(publicacoes);
		s.save(lp);
		
		s.getTransaction().commit();
		HibernateUtils.getSessionFactory().close();
		
	}
	
	
}
