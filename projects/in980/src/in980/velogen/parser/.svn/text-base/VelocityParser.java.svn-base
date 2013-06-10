package in980.velogen.parser;

import in980.velogen.file.FileUtil;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.Enumeration;
import java.util.Properties;

import org.apache.velocity.Template;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;

public class VelocityParser {

	private VelocityContext mainContext = null;
	private Template mainTemplate = null;	
	private final String TEMPLATE_ENCODING = "UTF-8";  //ISO-8859-1, UTF-8
//	private final String VELOCITY_PROPERTIES = "app/velocity.properties";
//	private final String VELOCITY_PROPERTIES = "/home/salaniojr/workspace-eclipse-galileo/testeweb/WebContent/template/velocity.properties";
	
	
	public VelocityParser(String templateFile) {
		try {
			Velocity.init();
			mainTemplate = Velocity.getTemplate(templateFile, TEMPLATE_ENCODING);
		} catch (Exception ex) {
			ex.printStackTrace();
			System.out.println("Error processing template file: "
					+ templateFile);
		}
	}

	public void addToContext(String key, Object value) {
		if (mainContext == null) {
			mainContext = new VelocityContext();
		}
		mainContext.put(key, value);
	}

	public void addToContext(VelocityContext chainCtx) {
		mainContext = new VelocityContext(chainCtx);
	}

	public VelocityContext getCurrentContext() {
		return mainContext;
	}

	public void processTemplate(OutputStreamWriter osw) {
		try {
			if (mainTemplate != null) {
				mainTemplate.merge(mainContext, osw);
			}
			osw.flush();
			osw.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public static void main(String[] args) throws IOException {
		Properties mainProps = FileUtil.getMainPropertiesFile();
		Enumeration<Object> keys = mainProps.keys();
		while (keys.hasMoreElements()) {
			String key = (String) keys.nextElement();
//			String auxKey = key + ".vm";
//			System.out.println(key);
			Properties p = FileUtil.getPropertiesFile((String) mainProps.get(key), args[1]); 
			FileUtil.prepareFile(key, p, args[0], args[1]);
		}				
	}
}