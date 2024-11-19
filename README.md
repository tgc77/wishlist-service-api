<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">SERVICES</h1></p>
<p align="center">
	<em><code>❯ LuizaLabs Wishlist API</code></em>
</p>
<p align="center">
	<!-- local repository, no metadata badges. --></p>
<p align="center">Built with the tools and technologies:</p>
<p align="center">
	<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=default&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>❯ This project is a new feature to manager wishlist's clients. </code>

---

##  Features

<code>❯ The API Gateway also provides managment of client's, products as access credentials.</code>

---

##  Project Structure

```sh
└── services/
    ├── clients
    │   ├── Dockerfile
    │   ├── api
    │   ├── main.py
    │   ├── requirements.txt
    │   └── run.sh
    ├── favorite_products
    │   ├── Dockerfile
    │   ├── api
    │   ├── main.py
    │   ├── requirements.txt
    │   └── run.sh
    ├── gateway
    │   ├── Dockerfile
    │   ├── api
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── run.sh
    │   └── tests
    └── products
        ├── Dockerfile
        ├── api
        ├── main.py
        ├── requirements.txt
        └── run.sh
```


###  Project Index
<details open>
	<summary><b><code>SERVICES/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			</table>
		</blockquote>
	</details>
	<details> <!-- clients Submodule -->
		<summary><b>clients</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/main.py'>main.py</a></b></td>
				<td><code>❯ Clients manager API entry point</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ Service container</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ depencencies</code></td>
			</tr>
			</table>
			<details>
				<summary><b>api</b></summary>
				<blockquote>
					<details>
						<summary><b>routers</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/routers/client.py'>client.py</a></b></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>core</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/settings.py'>settings.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/database.py'>database.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/error_handlers.py'>error_handlers.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/logger.py'>logger.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/utils.py'>utils.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/response.py'>response.py</a></b></td>
							</tr>
							</table>
							<details>
								<summary><b>entities</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/entities/client.py'>client.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/entities/token.py'>token.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>models</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/models/client.py'>client.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/models/types.py'>types.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>repositories</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/repositories/client.py'>client.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/repositories/repository.py'>repository.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>security</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/clients/api/core/security/user_authenticator.py'>user_authenticator.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- products Submodule -->
		<summary><b>products</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/main.py'>main.py</a></b></td>
				<td><code>❯ Products manager API entry point</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ Service container</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ Depencencies</code></td>
			</tr>
			</table>
			<details>
				<summary><b>api</b></summary>
				<blockquote>
					<details>
						<summary><b>core</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/database.py'>database.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/error_handlers.py'>error_handlers.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/logger.py'>logger.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/response.py'>response.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/settings.py'>settings.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/utils.py'>utils.py</a></b></td>
							</tr>
							</table>
							<details>
								<summary><b>entities</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/entities/product.py'>product.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>models</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/models/product.py'>product.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>repositories</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/repositories/product.py'>product.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>security</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/core/security/user_authenticator.py'>user_authenticator.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>routers</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/products/api/routers/product.py'>product.py</a></b></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- favorite_products Submodule -->
		<summary><b>favorite_products</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/main.py'>main.py</a></b></td>
				<td><code>❯ Favorite Products manager API entry point</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ Service containar</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ Dependencies</code></td>
			</tr>
			</table>
			<details>
				<summary><b>api</b></summary>
				<blockquote>
					<details>
						<summary><b>core</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/database.py'>database.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/error_handlers.py'>error_handlers.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/logger.py'>logger.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/response.py'>response.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/settings.py'>settings.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/utils.py'>utils.py</a></b></td>
							</tr>
							</table>
							<details>
								<summary><b>entities</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/entities/product.py'>product.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/entities/favorite_products.py'>favorite_products.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>models</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/models/product.py'>product.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/models/favorite_products.py'>favorite_products.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/models/client.py'>client.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>repositories</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/repositories/favorite_products.py'>favorite_products.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>security</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/core/security/user_authenticator.py'>user_authenticator.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>routers</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/favorite_products/api/routers/favorite_products.py'>favorite_products.py</a></b></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- gateway Submodule -->
		<summary><b>gateway</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/main.py'>main.py</a></b></td>
				<td><code>❯ API Gateway to manager credentials to access the APIs according user scopes </code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ Service container</code></td>
			</tr>
			<tr>
				<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ Dependencies</code></td>
			</tr>
			</table>
			<details>
				<summary><b>api</b></summary>
				<blockquote>
					<details>
						<summary><b>routers</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/routers/client.py'>client.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/routers/auth.py'>auth.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/routers/product.py'>product.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/routers/favorite_products.py'>favorite_products.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/routers/access_credentials.py'>access_credentials.py</a></b></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>core</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/database.py'>database.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/settings.py'>settings.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/error_handlers.py'>error_handlers.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/logger.py'>logger.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/utils.py'>utils.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/response.py'>response.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/__init.py'>__init.py</a></b></td>
							</tr>
							<tr>
								<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/initialize_models.py'>initialize_models.py</a></b></td>
							</tr>
							</table>
							<details>
								<summary><b>models</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/models/client.py'>client.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/models/access_credentials.py'>access_credentials.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>entities</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/entities/client.py'>client.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/entities/token.py'>token.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/entities/access_credentials.py'>access_credentials.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/entities/favorite_products.py'>favorite_products.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/entities/product.py'>product.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>repositories</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/repositories/access_credentials.py'>access_credentials.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/repositories/client.py'>client.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>security</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/security/user_authenticator.py'>user_authenticator.py</a></b></td>
									</tr>
									<tr>
										<td><b><a href='/home/tiago-zen/workspace/job-tests/luizalabs/wishlist/services/blob/master/gateway/api/core/security/password_crypt.py'>password_crypt.py</a></b></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with services, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python (3.10 >)
- **Package Manager:** Pip
- **Container Runtime:** Docker

###  Installation

Install services using the following method:

**Build from source:**

1. **Clone Locally**: Clone the repository to your local machine using a git client.
```sh
❯ git clone https://github.com/tgc77/wishlist-service-api.git
```

2. Enter directory root (whishlist) and rum make command:

**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)
```sh
❯ make build-up-api
```
It will build and starts the services containers and initialize database and models.

3. Wait until database-1 and gateway-1 containers finishs:
```sh
gateway-1            | INFO     Using import string main:app                                           
gateway-1            |                                                                                 
gateway-1            |  ╭─────────── FastAPI CLI - Production mode ───────────╮                        
gateway-1            |  │                                                     │                        
gateway-1            |  │  Serving at: http://0.0.0.0:8080                    │                        
gateway-1            |  │                                                     │                        
gateway-1            |  │  API docs: http://0.0.0.0:8080/docs                 │                        
gateway-1            |  │                                                     │                        
gateway-1            |  │  Running in production mode, for development use:   │                        
gateway-1            |  │                                                     │                        
gateway-1            |  │  fastapi dev                                        │                        
gateway-1            |  │                                                     │                        
gateway-1            |  ╰─────────────────────────────────────────────────────╯
gateway-1            | INFO:     Started server process [1]
gateway-1            | INFO:     Waiting for application startup.
gateway-1            | INFO:     Application startup complete.
gateway-1            | INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
gateway-1            | INFO:     127.0.0.1:44360 - "GET /api/gateway/healthchecker HTTP/1.1" 200 OK
```

4. Wait the other containers startup:
(products-1, client-1 and favorite_products-1) will show up similar messages as gateway-1 container

###  Usage
1. Access the swagger docs web page to interact with the API: http://0.0.0.0:8080/docs

2. To be able to acess the endpoints you will need to authenticate and get your access credentials.

3. To do that just click the green border Authorize buttom on the right top of the page.

4. There is already an api.admin user created in database, but perhaps the password has already expired.

5. Try to authenticated with the credentials:
- **username:** api.admin
- **password:** api.admin
- **scope:** admin

6. In case the credencials has already expired, just navegate to the endpoint:
- **Access Credentials:** PATCH /api/access/credentials/update/{client_id} Servicegatewayapiaccesscredentialsrouter. Update Access Credentials

## OBS: Dont forget to check the box admin scope option to get full access credentials.

###  Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```

---

##  Contributing

- **💬 [Join the Discussions](https://LOCAL/wishlist/services/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://LOCAL/wishlist/services/issues)**: Submit bugs found or log feature requests for the `services` project.
- **💡 [Submit Pull Requests](https://LOCAL/wishlist/services/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

