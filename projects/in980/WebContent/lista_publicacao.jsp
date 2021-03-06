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
	<h1><s:text name="lbl.toppage.listagemArtigos"/></h1>
	<form action="buscarPublicacoesPeloTitulo" method="get">
		<table>
			<tr>
				<td><s:text name="lbl.form.titulo"/></th>: <input type="text" size="15" name="tituloPublicacao" /> </td>
				<td><s:text name="lbl.form.ano"/></th>: <input type="text" size="15" name="ano" maxlength="4" /> </td>
				<td style="align:right" colspan="1"><input type="submit" value="Buscar" /> </td>				
			</tr>
		</table>
	</form>
	<br/>
	<br/>
	<hr/>
	<table border="0">
		<tr>
			<th></th>
			<th><s:text name="lbl.form.titulo"/></th>
			<th><s:text name="lbl.form.ano"/></th>
			<th>...</th>
			<th></th>
			<th></th>
			<th></th>
		</tr>
		<c:forEach items="${publicacoes}" var="publicacao">		
			<tr>
				<td></td>
				<td>
					${publicacao.titulo}
					(<a href="${publicacao.caminhoRelativoArquivo}">pdf</a>)
					(<a href="${publicacao.caminhoRelativoBibtex}">bib</a>)
				</td>
				<td>${publicacao.ano}</td>
				<td>&nbsp; ( ${publicacao.descTipo } ) &nbsp;</td>
				<td>...</td>
				<td>
					<c:set var="nomeDescritivo" value="${publicacao.nomeDescritivo}" />
					<a href="excluir${nomeDescritivo}?${nomeDescritivo}.ID=${publicacao.ID}">
						<s:text name="lbl.btn.excluir"/></th></a>
				</td>
				<td><a href="mostrar${nomeDescritivo}?${nomeDescritivo}.ID=${publicacao.ID}">
						<s:text name="lbl.btn.atualizar"/></th></a>
				</td>
			</tr>		
		</c:forEach>
		
	</table>
	<br/>
	<a href="index.jsp"><s:text name="lbl.paginaPrincipal" /></a>

</body>
</html>