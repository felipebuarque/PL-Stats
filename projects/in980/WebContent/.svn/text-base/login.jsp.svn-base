<?xml version="1.0" encoding="UTF-8" ?>
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="s" uri="/struts-tags"%>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>IN980 - RGMS</title>
</head>
<body>
<form action="autentica" method="post">
	<table>
		<tr>
			<td><s:text name="lbl.form.login" />:</td>
			<td><input type="text" name="usuario.login" size="10"
				maxlength="20" value="${usuario.login}" />
			</td>
		</tr>
		<tr>
			<td><s:text name="lbl.form.senha" />:</td>
			<td>
				<input type="password" name="usuario.senha" size="10"
				maxlength="8" value="${usuario.senha}" />
			</td>
		</tr>
		<tr>
			<td><input type="submit" value="Enviar" /></td>			
		</tr>		
	</table>
	${msg}
</form>
</body>
</html>