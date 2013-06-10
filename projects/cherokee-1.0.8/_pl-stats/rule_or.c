/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8 -*- */

/* Cherokee
 *
 * Authors:
 *      Alvaro Lopez Ortega <alvaro@alobbs.com>
 *
 * Copyright (C) 2001-2010 Alvaro Lopez Ortega
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of version 2 of the GNU General Public
 * License as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301, USA.
 */

#include "common-internal.h"
#include "rule_or.h"
#include "plugin_loader.h"
#include "virtual_server.h"

#define ENTRIES "rule,or"

PLUGIN_INFO_RULE_EASIEST_INIT(or);

static ret_t
match (cherokee_rule_t         *rule,
       cherokee_connection_t   *conn,
       cherokee_config_entry_t *ret_conf)
{
	ret_t ret;

	/* It only needs one of the sides to match.
	 */
	ret = cherokee_rule_match (RULE_OR(rule)->left, conn, ret_conf);
	if (ret != ret_not_found)
		return ret;

	/* It didn't match, it is time for the right side
	 */
	return cherokee_rule_match (RULE_OR(rule)->right, conn, ret_conf);
}

static ret_t
configure_branch (cherokee_rule_or_t        *rule,
		  cherokee_config_node_t    *conf,
		  cherokee_virtual_server_t *vsrv,
		  const char                *branch,
		  cherokee_rule_t          **branch_rule)
{
	ret_t                   ret;
	cherokee_config_node_t *subconf = NULL;

	/* Get the configuration sub-tree
	 */
	ret = cherokee_config_node_get (conf, branch, &subconf);
	if (ret != ret_ok)
		return ret;

	/* Instance the sub-rule match
	 */
	ret = cherokee_virtual_server_new_rule (vsrv, subconf,
						RULE(rule)->priority,
						branch_rule);
	if (ret != ret_ok)
		return ret;

	return ret_ok;
}

static ret_t
configure (cherokee_rule_or_t        *rule,
	   cherokee_config_node_t    *conf,
	   cherokee_virtual_server_t *vsrv)
{
	ret_t ret;

	ret = configure_branch (rule, conf, vsrv, "right", &rule->right);
	if (ret != ret_ok)
		return ret;

	ret = configure_branch (rule, conf, vsrv, "left", &rule->left);
	if (ret != ret_ok)
		return ret;

	return ret_ok;
}

static ret_t
_free (void *p)
{
	ret_t               ret;
	cherokee_rule_or_t *rule = RULE_OR(p);

	if (rule->left) {
		ret = cherokee_rule_free (rule->left);
		if (ret != ret_ok) return ret;
	}

	if (rule->right) {
		ret = cherokee_rule_free (rule->right);
		if (ret != ret_ok) return ret;
	}

	return ret_ok;
}

ret_t
cherokee_rule_or_new (cherokee_rule_t **rule)
{
	CHEROKEE_NEW_STRUCT (n, rule_or);

	/* Parent class constructor
	 */
	cherokee_rule_init_base (RULE(n), PLUGIN_INFO_PTR(or));

	/* Virtual methods
	 */
	RULE(n)->match     = (rule_func_match_t) match;
	RULE(n)->configure = (rule_func_configure_t) configure;
	MODULE(n)->free    = (module_func_free_t) _free;

	/* Properties
	 */
	n->left  = NULL;
	n->right = NULL;

	*rule = RULE(n);
	return ret_ok;
}

