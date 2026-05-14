from servicios.pipeline_rag import ejecutar_pipeline


if __name__ == "__main__":
    consulta = input("Consulta corporativa: ").strip()
    resultado = ejecutar_pipeline(consulta)
    print("\nRespuesta:")
    print(resultado["respuesta"])
    print("\nCitas:")
    for cita in resultado["citas"]:
        print(f"- {cita}")
