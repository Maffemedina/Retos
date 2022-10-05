Create database biblioteca

use biblioteca

CREATE TABLE Libros(
	codigo INT IDENTITY,
	titulo VARCHAR(40),
	autor VARCHAR(30),
	editorial VARCHAR(20),
	precio DECIMAL(5,2),
	cantidad SMALLINT,
	PRIMARY KEY(codigo)
)


CREATE PROCEDURE listar_libros
as
SELECT *
FROM Libros
ORDER BY codigo;


CREATE PROCEDURE buscar_libros
@titulo VARCHAR(40)
as
SELECT * 
FROM Libros
WHERE  (titulo LIKE + @titulo + '%');


CREATE PROCEDURE mantenimiento_libros
@codigo INT,
@titulo VARCHAR(40),
@autor VARCHAR(30),
@editorial VARCHAR(20),
@precio DECIMAL(5,2),
@cantidad SMALLINT,
@accion VARCHAR(50) OUTPUT
as
IF(@accion = '1') 
BEGIN
	INSERT INTO Libros
	VALUES(@titulo, @autor, @editorial, @precio, @cantidad)
	SET @accion = 'Se modifico el codigo: ' + CONVERT(varchar(10), @codigo)
END
ELSE IF(@accion = '2')
BEGIN
	UPDATE Libros SET titulo = @titulo, 
	autor = @autor, editorial = @editorial,
	precio = @precio, cantidad = @cantidad
	WHERE CONVERT(VARCHAR,codigo) = CONVERT(VARCHAR,@codigo)
	SET @accion = 'Se modifico el codigo: ' + CONVERT(varchar(10), @codigo)
END
ELSE IF(@accion = '3')
BEGIN
	DELETE FROM Libros WHERE (codigo = @codigo) 
	SET @accion = 'Se borro el registro con codigo: ' + CONVERT(varchar(10), @codigo)
END;
