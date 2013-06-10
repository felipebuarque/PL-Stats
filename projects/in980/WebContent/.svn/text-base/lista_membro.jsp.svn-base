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
	<h1><s:text name="lbl.toppage.listagemMembros" /></h1>
	<form action="buscarMembros" method="get">
		<table>
			<tr>
				<td><s:text name="lbl.form.nome" />: <input type="text" size="15" name="membro.nome" /> </td>
				<td><input type="submit" value="<s:text name="lbl.btn.buscar" />" /> </td>
			</tr>		
		</table>
	</form>
	<br/>
	<br/>
	<hr/>
	<table border="0">
		<tr>
			<th></th>
			<th><s:text name="lbl.form.nome" /></th>
			<th><s:text name="lbl.form.email" /></th>
			<th><s:text name="lbl.form.fone" /></th>
			<th><s:text name="lbl.form.universidade" /></th>
			<th><s:text name="lbl.form.website" /></th>
			<th><s:text name="lbl.form.situacao" /></th>
			<th></th>
			<th></th>
		</tr>
		<c:forEach items="${membros}" var="membro">		
			<tr>
				<td>
					<a href="paginaMembro?membro.ID=${membro.ID}"><img height="100" width="100" src="${membro.caminhoRelativoImagem}" alt="" /></a>
				</td>
				<td>${membro.nome}</td>
				<td>${membro.email}</td>
				<td>${membro.fone}</td>
				<td>${membro.universidade}</td>
				<td>${membro.website}</td>
				<td>
					<c:choose>
						<c:when test="${membro.ativo eq 0}">Ativo</c:when>
						<c:otherwise>Inativo</c:otherwise>
					</c:choose>
				</td>
				<td><a href="excluirMembro?membro.ID=${membro.ID}">
						<s:text name="lbl.btn.excluir"/></a>
				</td>
				<td><a href="mostrarMembro?membro.ID=${membro.ID}">
						<s:text name="lbl.btn.atualizar"/></a>
				</td>
			</tr>		
		</c:forEach>
		
	</table>
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>
</body>
</html>