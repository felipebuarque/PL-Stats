package in980.velogen.file;

import in980.velogen.parser.VelocityParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.Enumeration;
import java.util.Properties;

public class FileUtil {

	private static final String FILE_ENCODING = "ISO-8859-1"; // ISO-8859-1,
	// UTF-8
//	private static final String INPUT_DIR = "./input/";
//	private static final String OUTPUT_DIR = "./output/";
	private static final String APP_DIR = "./src/in980/velogen/app/";

	// private static final String DIR_IN =
	// "/home/salaniojr/workspace-eclipse-galileo/testeweb/WebContent/template/";
	// private static final String DIR_OUT =
	// "/home/salaniojr/workspace-eclipse-galileo/testeweb/WebContent/";

	public static Properties getPropertiesFile(String filePath, String input)
			throws IOException {
		return genericGetPropertiesFile(new File(input + filePath
				+ ".properties"));
	}

	public static Properties getMainPropertiesFile() throws IOException {
		return genericGetPropertiesFile(new File(APP_DIR + "tpltsprops"
				+ ".properties"));
	}

	private static Properties genericGetPropertiesFile(File file)
			throws IOException {
		Properties properties = new Properties();
		FileInputStream fis = new FileInputStream(file); // Ex.:
															// ./app/app.properties
		properties.load(fis);
		fis.close();
		return properties;
	}

	public static void prepareFile(String templateFilePath, Properties propFile, 
			String output, String input)
			throws IOException {
		VelocityParser velInstance = new VelocityParser(input
				+ templateFilePath + ".vm");

		Enumeration<Object> keys = propFile.keys();
		while (keys.hasMoreElements()) {
			String key = (String) keys.nextElement();
			velInstance.addToContext(key, propFile.get(key));
		}

		Charset cs = Charset.forName(FILE_ENCODING);
		OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream(
				output + templateFilePath + ".jsp"), cs);
		System.out.println(output + templateFilePath + ".jsp");

		velInstance.processTemplate(osw);
	}
}
