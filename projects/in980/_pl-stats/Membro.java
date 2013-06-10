package in980.rgms.domain;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.Serializable;
import java.nio.channels.FileChannel;
import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.Enumerated;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.OneToOne;
import javax.persistence.SequenceGenerator;
import javax.persistence.Transient;

@Entity
@SequenceGenerator(name = "membro_seq", sequenceName = "membro_seq")
public class Membro implements Serializable{

	private static final long serialVersionUID = 1L;
	
	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "membro_seq")
	private Integer ID;
	private String nome;
	private String email;
	private String fone;
	private String universidade;
	private String website;
	private Integer ativo;	
	private String foto;
	@Enumerated
	private Integer tipo;
	@ManyToMany(
			targetEntity=Publicacao.class,
			cascade={CascadeType.PERSIST, CascadeType.MERGE},
			mappedBy="autoresMembros", 
			fetch=FetchType.LAZY
	)
	private List<Publicacao> publicacoes;
	
	@ManyToMany(targetEntity = LinhaPesquisa.class, cascade = { CascadeType.PERSIST,
		CascadeType.MERGE }, fetch = FetchType.LAZY)
	@JoinTable(name = "membro_linhaPesquisa", joinColumns = @JoinColumn(name = "id_membro"), inverseJoinColumns = @JoinColumn(name = "id_linha_pesquisa"))
	private List<LinhaPesquisa> linhasPesquisa;

	@Transient
	private File upload;
	@Transient
	private String uploadFileName; // nome do arquivo enviado
	@Transient
	private String uploadContentType; // contexto do arquivo, imagem, txt etc...
	@Transient
	private String selected;

	public Membro() {
		super();
	}

	public Membro(Integer iD) {
		super();
		ID = iD;
	}
	
	// Metodo que move o arquivo para o diretorio desejado
    private void copyFile(File in, File out) {  	           
        try {  
            FileChannel sourceChannel = new FileInputStream(in).getChannel();  
            FileChannel destinationChannel = new FileOutputStream(out).getChannel();  
            sourceChannel.transferTo(0, sourceChannel.size(), destinationChannel);  
            sourceChannel.close();  
            destinationChannel.close();  
        } catch (IOException ex) {  
            ex.printStackTrace();   
        }  
    }  
    
    public void validateToPersist() throws Exception{
    	if(!getEmail().contains("@"))
    		throw new Exception("E-mail invalido");
    	if(getNome() == null)
    		throw new Exception("Nome invalido");
    	
    	foto = "/home/leofernandesmo/workspace/IN980-ResearchGroupManagementSystem/WebContent/fotosRGMS/"+ this.uploadFileName;
    		    	
//    	foto = "/home/salaniojr/workspace-eclipse-galileo/in980-rgms/in980-rgms/IN980-ResearchGroupManagementSystem/WebContent/fotosRGMS/"+ this.uploadFileName;
    	copyFile(upload, new File(foto));
    }

	@Override
	public String toString() {
		return nome;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getFone() {
		return fone;
	}

	public void setFone(String fone) {
		this.fone = fone;
	}

	public Integer getID() {
		return ID;
	}

	public void setID(Integer iD) {
		ID = iD;
	}

	public File getUpload() {
		return upload;
	}

	public void setUpload(File upload) {
		this.upload = upload;
	}

	public String getUploadFileName() {
		return uploadFileName;
	}

	public void setUploadFileName(String uploadFileName) {
		String extensao = uploadFileName.substring(uploadFileName.lastIndexOf("."));
		this.uploadFileName = getFone() +  "_" + extensao ;			
	}

	public String getUploadContentType() {
		return uploadContentType;
	}

	public void setUploadContentType(String uploadContentType) {
		this.uploadContentType = uploadContentType;
	}

	

	public String getUniversidade() {
		return universidade;
	}

	public void setUniversidade(String universidade) {
		this.universidade = universidade;
	}

	public String getWebsite() {
		return website;
	}

	public void setWebsite(String website) {
		this.website = website;
	}

	public Integer getAtivo() {
		return ativo;
	}

	public void setAtivo(Integer ativo) {
		this.ativo = ativo;
	}

	public String getFoto() {
		return foto;
	}

	public void setFoto(String foto) {
		this.foto = foto;
	}
	
	public String getCaminhoRelativoImagem() {
		if(getFoto() != null)
			return "fotosRGMS" + getFoto().substring(getFoto().lastIndexOf("/"));
		return null; 
	}

	public List<Publicacao> getPublicacoes() {
		return publicacoes;
	}

	public void setPublicacoes(List<Publicacao> publicacoes) {
		this.publicacoes = publicacoes;
	}

	public Integer getTipo() {
		return tipo;
	}

	public void setTipo(Integer tipo) {
		this.tipo = tipo;
	}



	public String getSelected() {
		return selected;
	}

	public void setSelected(String selected) {
		this.selected = selected;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((ID == null) ? 0 : ID.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Membro other = (Membro) obj;
		if (ID == null) {
			if (other.ID != null)
				return false;
		} else if (!ID.equals(other.ID))
			return false;
		return true;
	}

	public List<LinhaPesquisa> getLinhasPesquisa() {
		return linhasPesquisa;
	}

	public void setLinhasPesquisa(List<LinhaPesquisa> linhasPesquisa) {
		this.linhasPesquisa = linhasPesquisa;
	}
	
	//#ifdef autenticacao
//OneToOne(cascade={CascadeType.ALL}, fetch = FetchType.LAZY)
//	private Usuario usuario;
//	
//	public Usuario getUsuario() {
//		return usuario;
//	}
//	public void setUsuario(Usuario usuario) {
//		this.usuario = usuario;
//	}
	//#endif
	
}
