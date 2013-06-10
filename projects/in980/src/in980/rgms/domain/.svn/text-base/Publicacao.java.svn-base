package in980.rgms.domain;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Serializable;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.SequenceGenerator;
import javax.persistence.Transient;

@Entity
@SequenceGenerator(name = "publicacao_seq", sequenceName = "publicacao_seq")
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Publicacao implements Serializable {
	private static final long serialVersionUID = 1L;

	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "publicacao_seq")
	private Integer ID;
	private Integer ano;
	private String titulo;
	@ManyToMany(targetEntity = Membro.class, cascade = { CascadeType.PERSIST,
			CascadeType.MERGE }, fetch = FetchType.EAGER)
	@JoinTable(name = "publicacao_membro", joinColumns = @JoinColumn(name = "id_publicacao"), inverseJoinColumns = @JoinColumn(name = "id_membro"))
	private List<Membro> autoresMembros;
	
	@ManyToMany(targetEntity = LinhaPesquisa.class, cascade = { CascadeType.PERSIST,
		CascadeType.MERGE }, fetch = FetchType.LAZY)
	@JoinTable(name = "publicacao_linhaPesquisa", joinColumns = @JoinColumn(name = "id_publicacao"), inverseJoinColumns = @JoinColumn(name = "id_linha_pesquisa"))
	private List<LinhaPesquisa> linhasPesquisa;
	
	private String autoresNaoMembros;
	private String filePath;

	@Transient
	private File upload;
	@Transient
	private String uploadFileName; // nome do arquivo enviado
	@Transient
	private String uploadContentType; // contexto do arquivo, imagem, txt etc...

	public abstract String getDescTipo();

	public abstract String getNomeDescritivo();

	protected abstract void validateSubToPersist() throws Exception;

	public void validateToPersist() throws Exception {
		if (getTitulo() == null || getTitulo().isEmpty())
			throw new Exception("Titulo Invalido");
		if (getAno() == null)
			throw new Exception("Ano invalido");
		if (getUploadFileName() == null
				|| !getUploadFileName().contains(".pdf"))
			throw new Exception("Arquivo Invalido (Obrigatorio formato PDF)");

		validateSubToPersist();
		
    	filePath = "/home/leofernandesmo/workspace/IN980-ResearchGroupManagementSystem/WebContent/artigosRGMS/"+ this.uploadFileName;

//		filePath = "/home/salaniojr/workspace-eclipse-galileo/in980-rgms/in980-rgms/IN980-ResearchGroupManagementSystem/WebContent/artigosRGMS/"
//				+ this.uploadFileName;
		
		copyFile(upload, new File(filePath));
		geraBibtexFile();
	}

	// Metodo que move o arquivo para o diretorio desejado
	private void copyFile(File in, File out) {
		try {
			FileChannel sourceChannel = new FileInputStream(in).getChannel();
			FileChannel destinationChannel = new FileOutputStream(out)
					.getChannel();
			sourceChannel.transferTo(0, sourceChannel.size(),
					destinationChannel);
			sourceChannel.close();
			destinationChannel.close();
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
	
	public void geraBibtexFile(){
		String arquivo = "/home/leofernandesmo/workspace/IN980-ResearchGroupManagementSystem/WebContent/artigosRGMS/"
			+ this.uploadFileName;
		arquivo = arquivo.substring(0, arquivo.lastIndexOf("."));
				
		try {
			FileWriter writer = new FileWriter(arquivo + ".bib");
			PrintWriter saida = new PrintWriter(writer);
			adicionaInfoBibtex(saida);
			saida.close();
			writer.close();			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected abstract void adicionaInfoBibtex(PrintWriter saida) ;

	public Integer getAno() {
		return ano;
	}

	public void setAno(Integer ano) {
		this.ano = ano;
	}

	public String getTitulo() {
		return titulo;
	}

	public void setTitulo(String titulo) {
		this.titulo = titulo;
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
		this.uploadFileName = uploadFileName;
	}

	public String getUploadContentType() {
		return uploadContentType;
	}

	public void setUploadContentType(String uploadContentType) {
		this.uploadContentType = uploadContentType;
	}

	public String getFilePath() {
		return filePath;
	}

	public void setFilePath(String filePath) {
		this.filePath = filePath;
		String nomeArquivo = filePath.substring(filePath.lastIndexOf("/") + 1);
		setUploadFileName(nomeArquivo);
	}

	public List<Membro> getAutoresMembros() {
		return autoresMembros;
	}

	public void setAutoresMembros(List<Membro> autoresMembros) {
		this.autoresMembros = autoresMembros;
	}

	public void addAutorMembro(Membro m) {
		this.autoresMembros.add(m);
	}

	public String getAutoresNaoMembros() {
		return autoresNaoMembros;
	}

	public void setAutoresNaoMembros(String autoresNaoMembros) {
		this.autoresNaoMembros = autoresNaoMembros;
	}

	public String getCaminhoRelativoArquivo() {
		if (getFilePath() != null)
			return "artigosRGMS"
					+ getFilePath().substring(getFilePath().lastIndexOf("/"));

		return null;
	}
	
	public String getCaminhoRelativoBibtex() {
		if (getFilePath() != null){
			String arquivoBib = "artigosRGMS"
				+ getFilePath().substring(getFilePath().lastIndexOf("/"));
			arquivoBib = arquivoBib.replaceAll(".pdf", ".bib");
			return arquivoBib;
		}

		return null;
	}

	public List<String> getListAutoresNaoMembros() {
		if (getAutoresNaoMembros() != null) {
			List<String> lista = new ArrayList<String>();
			String[] autores = getAutoresNaoMembros().split(",");
			for (String autor : autores) {
				lista.add(autor);
			}
			return lista;
		}
		return null;
	}
	
	protected String getStringAutoresMembros(){
//		StringBuilder strAutores = new StringBuilder();
//		for (Membro m : getAutoresMembros()) {
//			strAutores.append(m.getNome());
//			strAutores.append(", ");
//		}
//		return strAutores.toString();
		return "";
	}

	public List<LinhaPesquisa> getLinhasPesquisa() {
		return linhasPesquisa;
	}

	public void setLinhasPesquisa(List<LinhaPesquisa> linhasPesquisa) {
		this.linhasPesquisa = linhasPesquisa;
	}

	

}
