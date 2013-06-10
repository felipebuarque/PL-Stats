<?xml version="1.0" encoding="UTF-8" ?>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>   
 <%@ taglib prefix="s" uri="/struts-tags" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>IN980 - RGMS</title>
</head>
<body>
	<h1><s:text name="lbl.toppage.listagemLinhaPesquisa" /></h1>
	<form action="buscarLinhasPesquisa" method="get">
		<table>
			<tr>
				<td><s:text name="lbl.form.descricao" />: <input type="text" size="15" name="linhaPesquisa.descricao" /> </td>
				<td><input type="submit" value="<s:text name="lbl.btn.buscar" />" /> </td>
			</tr>		
		</table>
	</form>
	<br/>
	<br/>
	<hr/>
	<table border="0">
		<tr>
			<th><s:text name="lbl.form.titulo" /></th>
			<th><s:text name="lbl.form.descricao" /></th>			
			<th></th>
			<th></th>
		</tr>
		<c:forEach items="${linhasPesquisa}" var="linhaPesquisa">		
			<tr>
				<td>${linhaPesquisa.titulo}</td>
				<td>${linhaPesquisa.descricao}</td>
				<td><a href="excluirLinhaPesquisa?linhaPesquisa.ID=${linhaPesquisa.ID}">
						<s:text name="lbl.btn.excluir"/></a>
				</td>
				<td><a href="mostrarLinhaPesquisa?linhaPesquisa.ID=${linhaPesquisa.ID}">
						<s:text name="lbl.btn.atualizar"/></a>
				</td>
			</tr>		
		</c:forEach>
		
	</table>
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>